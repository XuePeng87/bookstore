import request from '@/config/axios'

export const queryByISBN = (isbn: string) => {
  return request.get({ url: '/query/' + isbn })
}

export const query = (params: any) => {
  return request.get({ url: '/books', params })
}

export const queryById = (id: string) => {
  return request.get({ url: '/books/' + id })
}

export const create = (data: any): Promise<IResponse> => {
  return request.post({ url: '/books', data })
}

export const update = (id: string, data: any): Promise<IResponse> => {
  return request.put({ url: '/books/' + id, data })
}

export const remove = (id: string): Promise<IResponse> => {
  return request.delete({ url: '/books/' + id })
}
