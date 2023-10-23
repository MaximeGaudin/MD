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
                         :disabled="loading"
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
                         :disabled="loading"
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
                        :disabled="loading"
                        v-model="query"
              >
                df.head()
              </textarea>
            </div>
          </div>

          <div class="mt-6 flex items-center justify-end gap-x-6">
            <div v-if="loading" role="status">
              <svg aria-hidden="true" class="w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
                   viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path
                    d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                    fill="currentColor"/>
                <path
                    d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                    fill="currentFill"/>
              </svg>
              <span class="sr-only">Loading...</span>
            </div>

            <button type="submit"
                    :disabled="loading"
                    class="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
              Run
            </button>
          </div>

          <div v-if="error" class="text-red-500 font-bold">
            {{ error }}
          </div>

          <ResultDisplay v-if="queryResult" :query-result="queryResult"/>
        </div>
      </div>
    </div>

  </form>
</template>

<script setup lang="ts">

import {ref} from "vue";
import {runQuery} from "../services/studio.service.ts";
import ResultDisplay from "../components/ResultDisplay.vue";

const year = ref(2021)
const month = ref(4)
const query = ref("df.head()")

const queryResult = ref()
const error = ref()

const loading = ref(false)

const displayQueryResult = async () => {
  loading.value = true
  error.value = null
  queryResult.value = null

  runQuery({
    year: year.value,
    month: month.value,
    query: query.value
  })
      .then((r) => queryResult.value = r)
      .catch((e) => error.value = e.response.data)
      .finally(() => loading.value = false)
}
</script>


<style scoped>

</style>