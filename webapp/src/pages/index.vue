<template>
  <form @submit.prevent="displayQueryResult">
    <div class="space-y-12">
      <div class="pb-4">
        <h2 class="text-2xl font-semibold leading-7 text-gray-900">Studio</h2>
        <p class="mt-1 text-sm leading-6 text-gray-600">Write & Debug your queries here before running them in schedule
          jobs.</p>

        <div class="mt-10">
          <div class="w-full flex mb-6">
            <div class="sm:col-span-4 mr-4">
              <label for="year" class="block text-sm font-medium leading-6 text-gray-900">Year</label>
              <div class="mt-2">
                <div
                    class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                  <input type="number" name="year" id="year"
                         class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                         min="2000"
                         max="2050"
                         placeholder="2023"
                         required
                         v-model="year"
                  />
                </div>
              </div>
            </div>
            <div class="sm:col-span-4">
              <label for="month" class="block text-sm font-medium leading-6 text-gray-900">Month</label>
              <div class="mt-2">
                <div
                    class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                  <input type="number" name="month" id="month"
                         class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                         min="1"
                         max="12"
                         placeholder="4"
                         required
                         v-model="month"
                  />
                </div>
              </div>
            </div>
          </div>

          <div class="col-span-full">
            <label for="query" class="block text-sm font-medium leading-6 text-gray-900">Pandas Query</label>
            <div class="mt-2">
              <textarea id="query" name="query" rows="3"
                        class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                        required
                        v-model="query"
              >
                df.head()
              </textarea>
            </div>
          </div>

          <div class="mt-6 flex items-center justify-end gap-x-6">
            <button type="submit"
                    class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
              Run
            </button>
          </div>

          <div v-if="error" class="text-red-500 font-bold">
            {{ error }}
          </div>

          <div v-if="queryResult" class="mt-8">
            <PandaTable :queryResult="queryResult"
            />
          </div>
        </div>
      </div>
    </div>

  </form>
</template>

<script setup lang="ts">

import PandaTable from "../components/PandaTable.vue";
import {ref} from "vue";
import {runQuery} from "../services/studio.service.ts";

const year = ref(2021)
const month = ref(4)
const query = ref("df.head()")

const queryResult = ref()
const error = ref()

const displayQueryResult = async () => {
  error.value = null
  queryResult.value = null

  runQuery({
    year: year.value,
    month: month.value,
    query: query.value
  })
      .then((r) => queryResult.value = r)
      .catch((e) => error.value = e.response.data)
}
</script>


<style scoped>

</style>