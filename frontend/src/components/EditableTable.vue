<template>
  <EasyDataTable
      :headers="headers"
      :items="items"
      :body-row-class-name="bodyRowClassName"
      :search-field="searchField"
      :search-value="searchValue"
      alternating
      border-cell
  > 
      <template #expand="item" v-if="$slots.expand">
          <slot
            name="expand"
            v-bind="item"
          />
      </template>
      <template
          v-for="header in headers.filter(h => h.editable)"
          #[`item-${header.value}`]="item"
      >
          <EditableCell
              :value="item[header.value]"
              :type="header.type"
              :match="header.match"
              @update="$emit('updateField', {'field': header.value, 'id': item.id, 'value': formatValue($event, header)})"
          />
      </template>
      <template
          v-for="slot in Object.keys($slots).filter(s => s.startsWith('item-'))"
          #[slot]="item"
      >
      <slot :name="slot" v-bind="item" />
      </template>
  </EasyDataTable>
</template>

<script lang="ts">
import {defineComponent, onMounted, ref, PropType} from 'vue';
import type {Header, Item} from "vue3-easy-data-table";
import EditableCell from "./EditableCell.vue";

export { Item };

export interface EditableTableHeader extends Header {
    editable?: boolean,
    type?: string,
    match?: string,
    float_precision?: number,
    max?: number,
    min?: number,
}

export default defineComponent({
  props: {
    headers: {
      type: Array as PropType<EditableTableHeader[]>,
      required: true,
    },
    items: {
      type: Array as PropType<Item[]>,
      required: true,
    },
    bodyRowClassName: {
      type: Function as PropType<(item: Item, rowNumber: number) => string>,
      required: false,
      default: () => '',
    },
    searchField: {
      type: [String, Array],
      default: '',
    },
    searchValue: {
      type: String,
      default: '',
    },
  },
  components: {
    EditableCell,
  },
  methods: {
    formatValue(value: string, header: EditableTableHeader) {
      if (header.type === 'number') {
        if (!parseFloat(value)) {
          return '0';
        }
        if (header.max && parseFloat(value) > header.max) {
          return header.max.toString();
        }
        if (header.min && parseFloat(value) < header.min) {
          return header.min.toString();
        }
        if (header.float_precision) {
          return parseFloat(value).toFixed(header.float_precision);
        }
      }
      return value;
    },
  },
});
</script>

<style>
.input-wrapper {
  padding: 2px;
  box-sizing: border-box;
  max-height: 3em !important;
  overflow: hidden !important;
  display: flex !important;
  align-items: center !important;
  line-height: 1.5 !important;
  border: none !important;
}

.input-wrapper input {
  box-sizing: border-box !important;
  max-height: 100% !important;
  width: 100% !important;
  white-space: pre-wrap !important;
  word-wrap: break-word !important;
  line-height: inherit !important;
  border: none !important;
  outline: none !important;
}
</style>
