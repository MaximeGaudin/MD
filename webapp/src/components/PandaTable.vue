<template>
  <div class="mt-8 flow-root">
    <div class="-mx-4 -my-2  sm:-mx-6 lg:-mx-8">
      <div class="inline-block max-w-full w-fullpy-2 align-middle sm:px-6 lg:px-8">
        <table class="max-w-full w-full divide-y divide-gray-300">
          <thead>
          <tr>
            <th v-for="column in columns" :key="'col-' + column" scope="col"
                class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0">
              {{ column }}
            </th>
          </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
          <tr v-for="index in indices" :key="index">
            <td v-for="column in columns" class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{
                queryResult[column][index]
              }}
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

const props = defineProps<{
  queryResult: any
}>()

const indices = Object.keys(props.queryResult[Object.keys(props.queryResult)[0]])
const columns = Object.keys(props.queryResult)
</script>