import pymupdf
import re
from .database import Profession
from enum import Enum
from functools import reduce
import locale

def _convert(text: str) -> list[Profession]:
    proffesions_match = re.findall(r'(\d{4}-\d{3})\$(.+?)\$(\d\d)((?:\$[\d, Б/р–]+)+)(?:$|\$)', text)
    if not proffesions_match:
        return None
    proffesions = []
    for match in proffesions_match:
        education_length = match[3].strip('$')
        education_length = education_length.split('$')
        education_category = education_length[len(education_length) // 2:]
        education_length = education_length[:len(education_length) // 2]
        name = match[1]
        name = name.replace('$', ' ') if name.find('$') != -1 and name[name.find('$') - 1] != '-' else name.replace('$', '')
        proffesions.append(Profession(
            code = match[0],
            name = name,
            etks = match[2],
            education_durations = education_length,
            education_categories = education_category
        ))
    return proffesions

class _Profession_Patch_Action(Enum):
    REPLACE = 1
    APPEND = 2
    REMOVE = 3

class _Profession_Patch:
    def __init__(self, action: _Profession_Patch_Action, profession: Profession | str, profession2: Profession | str | None = None):
        self.action = action
        self.profession = profession
        self.profession2 = profession2

    def transform(self):
        if isinstance(self.profession, Profession):
            return []
        patches = []
        self.profession = _convert(self.profession)
        if self.profession2:
            self.profession2 = _convert(self.profession2)
        if len(self.profession) > 1:
            for profession, profession2 in zip(self.profession[1:], self.profession2[1:]):
                patches.append(_Profession_Patch(self.action, profession, profession2))
        self.profession = self.profession[0]
        if self.profession2:
            self.profession2 = self.profession2[0]
        return patches

def _load_patches_file(path: str) -> list[_Profession_Patch]:
    pdf = pymupdf.open(path)
    patches = []
    current = ''
    for page in pdf.pages(0, 49):
        blocks = page.get_textpage().extractDICT()['blocks']
        lines = reduce(lambda l, v: l + v['lines'], blocks, [])
        for line in lines:
            text = line['spans'][0]['text'].strip().replace('*** ', '$')
            if re.match(r'^«\d{4}-\d{3}', text):
                if current != '':
                    patches[-1].profession2 = current.strip('$').strip(';').strip('«').strip('»')
                current = text + '$'
            elif text.startswith('заменить'):
                patches.append(_Profession_Patch(_Profession_Patch_Action.REPLACE, current.strip('$').strip(';').strip('«').strip('»')))
                current = ''
            elif text.startswith('дополнить позицией'):
                patches.append(_Profession_Patch(_Profession_Patch_Action.APPEND, current.strip('$').strip(';').strip('«').strip('»')))
                current = ''
            elif text.startswith('исключить'):
                patches.append(_Profession_Patch(_Profession_Patch_Action.REMOVE, current.strip('$').strip(';').strip('«').strip('»')))
                current = ''
            elif current == '' or text == '' or current.endswith(';$') or current.endswith('»$'):
                continue
            else:
                current += text + '$'

    if current != '':
        patches[-1].profession2 = current.strip('$').strip(';').strip('«').strip('»')

    pdf.close()

    return patches

def _load_document(path: str) -> list[Profession]:
    pdf = pymupdf.open(path)
    professions = []
    for page in pdf:
        blocks = page.get_textpage().extractDICT()['blocks']
        lines = reduce(lambda l, v: l + v['lines'], blocks, [])
        current = ''
        for line in lines:
            text = line['spans'][0]['text'].strip()
            if re.match(r'^\d{4}-\d{3}$', text):
                if current != '':
                    professions.append(current.strip('$'))
                current = text + '$'
            elif current != '':
                current += text + '$'

        if current != '':
            professions.append(current.strip('$'))

    professions = list(map(lambda profession: _convert(profession).pop(), professions))

    pdf.close()

    return professions

def _patch_professions(patches: list[_Profession_Patch], professions: list[Profession]):
    for patch in patches:
        match patch.action:
            case _Profession_Patch_Action.REPLACE:
                for i in range(len(professions)):
                    if patch.profession.name.lower() == professions[i].name.lower():
                        professions[i] = patch.profession2
                        break
            case _Profession_Patch_Action.APPEND:
                for i in range(len(professions)):
                    if patch.profession.name.lower() == professions[i].name.lower():
                        professions.insert(i + 1, patch.profession2)
                        break
            case _Profession_Patch_Action.REMOVE:
                for i in range(len(professions)):
                    if patch.profession.name.lower() == professions[i].name.lower():
                        professions.pop(i)
                        break

def load_documents(patch_path: str, document_path: str) -> list[Profession]:
    patches = _load_patches_file(patch_path)
    for patch in patches:
        additional_patches = patch.transform()
        patches.extend(additional_patches)

    professions = _load_document(document_path)
    _patch_professions(patches, professions)

    return professions
