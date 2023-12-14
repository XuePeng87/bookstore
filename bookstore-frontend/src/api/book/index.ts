import request from '@/config/axios'

export const queryByISBN = (isbn: string): Promise<IResponse> => {
  return request.get({ url: 'http://127.0.0.1:8000/query/' + isbn })
}

export const query = (params: any): Promise<IResponse> => {
  return request.get({ url: 'http://127.0.0.1:8000/books', params })
}

export const queryById = (id: string): Promise<IResponse> => {
  return request.get({ url: 'http://127.0.0.1:8000/books/' + id })
}

export const create = (data: any): Promise<IResponse> => {
  return request.post({ url: 'http://127.0.0.1:8000/books', data })
}

export const update = (id: string, data: any): Promise<IResponse> => {
  return request.put({ url: 'http://127.0.0.1:8000/books/' + id, data })
}

export const remove = (id: string): Promise<IResponse> => {
  return request.delete({ url: 'http://127.0.0.1:8000/books/' + id })
}

export const queryClcs = (): Promise<IResponse> => {
  return request.get({ url: 'http://127.0.0.1:8000/types' })
}

export const queryTags = (): Promise<IResponse> => {
  return request.get({ url: 'http://127.0.0.1:8000/tags' })
}
