import axios from "axios";

export type Query = {
    id: number,
    name: string,
    query: string,
}

export type NewQueryRequest = {
    name: string,
    query: string,
}

export const getAllQueries = async () => {
    return (await axios.get<Query[]>(`/api/queries`)).data
}

export const saveQuery = async (request: NewQueryRequest) => {
    return (await axios.post(`/api/queries`, request)).data
}

export const deleteQuery = async (id: number) => {
    await axios.delete(`/api/queries/${id}`)
}