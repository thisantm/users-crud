export interface Todo {
  id: number
  content: string
}

export interface Meta {
  totalCount: number
}

export interface User {
  _id: string
  username: string
  roles: string[]
  preferences: {
    timezone: string
  }
  active: boolean
  created_ts: Date
}
