import axios from 'axios'
import { defineStore } from 'pinia'
import type { User } from 'src/components/models'

const apiUrl = import.meta.env.VITE_API_URL

interface UserRequest {
  username: string
  roles: string[]
  preferences: {
    timezone: string
  }
  active: boolean
}

const usersStore = defineStore('usersStore', {
  actions: {
    async fetchUsers() {
      try {
        const response = await axios.get(`${apiUrl}/users?skip=0&limit=1000000`)
        return response.data as User[]
      } catch (error) {
        console.error('Error fetching users:', error)
      }
    },
    async fetchUserById(id: string) {
      try {
        const response = await axios.get(`${apiUrl}/users/${id}`)
        return response.data as User[]
      } catch (error) {
        if (axios.isAxiosError(error)) {
          if (error.response?.status === 404) {
            throw new Error('User not found')
          } else if (error.response?.status === 500) {
            throw new Error('Server error')
          }
        }
        console.error('Error fetching user:', error)
      }
    },
    async createUser(user: User) {
      try {
        const userRequest = {
          username: user.username,
          roles: user.roles,
          preferences: {
            timezone: user.preferences.timezone
          },
          active: user.active
        } as UserRequest
        const response = await axios.post(`${apiUrl}/users`, userRequest)
        return response.data as User
      } catch (error) {
        console.error('Error creating user:', error)
      }
    },
    async updateUser(user: User) {
      try {
        const userRequest = {
          username: user.username,
          roles: user.roles,
          preferences: {
            timezone: user.preferences.timezone
          },
          active: user.active
        } as UserRequest
        const response = await axios.put(`${apiUrl}/users/${user._id}`, userRequest)
        return response.data as User
      } catch (error) {
        console.error('Error updating user:', error)
      }
    },
    async deleteUser(id: string) {
      try {
        const response = await axios.delete(`${apiUrl}/users/${id}`)
        return response.data as User
      } catch (error) {
        console.error('Error deleting user:', error)
      }
    }
  }
})

export default usersStore
