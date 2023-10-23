import axios from "axios";

type RunQueryRequest = {
    year: number,
    month: number,
    query: string
}

export const runQuery = async (request: RunQueryRequest) => {
    return (await axios.post(`/api/query`, request)).data
}

export enum DisplayMode {
    TABLE,
    JSON,
    LIST,
}