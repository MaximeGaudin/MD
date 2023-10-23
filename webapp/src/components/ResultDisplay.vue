<template>
  <div v-if="queryResult">
    <div>
      <label for="display" class="block text-sm font-medium leading-6 text-gray-900">Display</label>
      <select id="display" name="display"
              v-model="display"
              class="mt-2 block w-full rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
        <option v-for="display in displayModes" :value="display.value">{{ display.name }}</option>
      </select>
    </div>

    <div v-if="queryResult && display == DisplayMode.TABLE" class="mt-8">
      <PandaTable :queryResult="queryResult"/>
    </div>

    <div v-if="queryResult && display == DisplayMode.LIST" class="mt-8">
      <ul>
        <li v-for="key in Object.keys(queryResult)" :key="key">{{ key }} : {{ queryResult[key] }}</li>
      </ul>
    </div>

    <div v-if="queryResult && display == DisplayMode.JSON" class="mt-8">
      <pre>{{ JSON.stringify(queryResult, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup lang="ts">

import {ref} from "vue";
import PandaTable from "./PandaTable.vue";
import {DisplayMode} from "../services/studio.service.ts";


const display = ref(DisplayMode.LIST)
const displayModes = [
  {
    name: "Table",
    value: DisplayMode.TABLE
  },
  {
    name: "List",
    value: DisplayMode.LIST
  },
  {
    name: "Json",
    value: DisplayMode.JSON
  },
]

defineProps<{
  queryResult: any
}>()

</script>
<style scoped>

</style>