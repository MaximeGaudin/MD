<template>
  <div class="space-y-12">
    <div class="pb-4">
      <div class="sm:flex sm:items-center">
        <div class="sm:flex-auto">
          <h1 class="text-2xl font-semibold leading-6 text-gray-900">Analyses</h1>
          <p class="mt-2 text-sm text-gray-700">Manage all your queries</p>
        </div>
        <div class="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <button type="button"
                  @click="modalOpen=true"
                  class="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">
            Add query
          </button>
        </div>
      </div>

      <div class="mt-10">
        <div class="mt-8 flow-root">
          <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
              <table class="min-w-full divide-y divide-gray-300">
                <thead>
                <tr>
                  <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-0">ID
                  </th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Name</th>
                  <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Query</th>
                  <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-0">
                    <span class="sr-only">Delete</span>
                  </th>
                </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                <tr v-for="query in queries" :key="query.id">
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ query.id }}</td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ query.name }}</td>
                  <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ query.query }}</td>
                  <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-0">
                    <a href="#"
                       @click="runQueryAndDisplayResult(query.query)"
                       class="text-indigo-600 hover:text-indigo-900 mr-10"
                    >Run<span class="sr-only"></span></a>

                    <a href="#"
                       @click="deleteQueryAndRefresh(query.id)"
                       class="text-indigo-600 hover:text-indigo-900"
                    >Delete<span class="sr-only"></span></a>
                  </td>
                </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <ResultDisplay class="mt-10" :query-result="queryResult"/>
    </div>

    <Modal :open="modalOpen">
      <form @submit.prevent="saveQueryAndCloseModal">
        <div class="">
          <div class="pb-4">
            <div class="grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
              <div class="col-span-full">
                <label for="name" class="block text-sm font-medium leading-6 text-gray-900">Name</label>
                <div class="mt-2">
                  <div
                      class="flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-indigo-600 sm:max-w-md">
                    <input type="text" name="name" id="name"
                           class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                           required
                           v-model="newQueryName"
                    />
                  </div>
                </div>
              </div>

              <div class="col-span-full">
                <label for="query" class="block text-sm font-medium leading-6 text-gray-900">Query</label>
                <div class="mt-2">
                  <textarea id="query" name="query" rows="3"
                            class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            required
                            v-model="newQueryValue"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-5 sm:mt-6 sm:grid sm:grid-flow-row-dense sm:grid-cols-2 sm:gap-3">
          <button type="submit"
                  class="inline-flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 sm:col-start-2"
          >Save
          </button>
          <button type="button"
                  class="mt-3 inline-flex w-full justify-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50 sm:col-start-1 sm:mt-0"
                  @click="closeModal" ref="cancelButtonRef">Cancel
          </button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import Modal from "../components/Modal.vue";
import {ref} from "vue";
import {deleteQuery, getAllQueries, Query, saveQuery} from "../services/analyses.service.ts";
import {runQuery} from "../services/studio.service.ts";
import ResultDisplay from "../components/ResultDisplay.vue";

const modalOpen = ref(false)
const newQueryValue = ref("")
const newQueryName = ref("")

const queries = ref<Query[]>([])

const queryResult = ref("")

const saveQueryAndCloseModal = async () => {
  await saveQuery({
    name: newQueryName.value,
    query: newQueryValue.value
  })

  queries.value = await getAllQueries()
  closeModal()
}

const closeModal = () => {
  modalOpen.value = false
  newQueryValue.value = ""
  newQueryName.value = ""
}

const deleteQueryAndRefresh = async (id: number) => {
  await deleteQuery(id)
  queries.value = await getAllQueries()
  queryResult.value = null
}

const runQueryAndDisplayResult = async (query: string) => {
  queryResult.value = null

  runQuery({
    year: 2021,
    month: 4,
    query: query
  })
      .then((r) => queryResult.value = r)
      .catch((e) => console.log(e))
}

queries.value = await getAllQueries()
</script>


<style scoped>

</style>