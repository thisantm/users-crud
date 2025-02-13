<template>
  <div class="container">
    <div v-if="user">
      <h1>{{ user.username }}</h1>
      <p>ID: {{ user._id }}</p>
      <p>Active: {{ user.active }}</p>
      <p>Created: {{ user.created_ts }}</p>
      <p>Timezone: {{ user.preferences?.timezone }}</p>
      <p>Roles: {{ user.roles.join(', ') }}</p>
      <div class="button-group">
        <q-btn
          @click="goHome"
          color="green"
          >Return to HomePage</q-btn
        >
        <q-btn
          @click="openUserDialog(user)"
          color="primary"
          >Edit User</q-btn
        >
        <q-btn
          @click="confirmDeleteUser(user._id)"
          color="negative"
          >Delete User</q-btn
        >
      </div>
    </div>
    <div v-else>
      <p>Loading...</p>
    </div>
    <UserDialog
      :visible="isUserDialogVisible"
      :user="selectedUser"
      @update:visible="isUserDialogVisible = $event"
      @submit="handleUserSubmit"
    />
    <DeleteDialog
      :visible="isDeleteDialogVisible"
      @update:visible="isDeleteDialogVisible = $event"
      @confirm="deleteUser"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import type { User } from 'components/models'
import usersStore from 'src/stores/users-store'
import UserDialog from 'src/components/UserDialog.vue'
import DeleteDialog from 'src/components/DeleteDialog.vue'

const user = ref<User | null>(null)
const route = useRoute()
const router = useRouter()
const usersStoreCalls = usersStore()

const isUserDialogVisible = ref(false)
const selectedUser = ref<User | null>(null)
const isDeleteDialogVisible = ref(false)
const userIdToDelete = ref<string | null>(null)

const goHome = async () => {
  await router.push('/')
}

const openUserDialog = (user: User | null = null) => {
  selectedUser.value = user
  isUserDialogVisible.value = true
}

const handleUserSubmit = async (userData: User) => {
  if (selectedUser.value) {
    await usersStoreCalls.updateUser(userData)
    console.log('Editing user:', userData)
  }
  isUserDialogVisible.value = false
  const fetchedUsers = await usersStoreCalls.fetchUserById(userData._id)
  user.value = (fetchedUsers && fetchedUsers.length > 0 ? fetchedUsers[0] : null) as User
}

const confirmDeleteUser = (userId: string) => {
  userIdToDelete.value = userId
  isDeleteDialogVisible.value = true
}

const deleteUser = async () => {
  if (userIdToDelete.value) {
    await usersStoreCalls.deleteUser(userIdToDelete.value)
    userIdToDelete.value = null
    isDeleteDialogVisible.value = false
    await goHome()
  }
}

onBeforeMount(async () => {
  const userId = route.params.id as string
  try {
    const users = await usersStoreCalls.fetchUserById(userId)
    user.value = (users && users.length > 0 ? users[0] : null) as User | null
    if (!user.value) {
      await router.push({ name: 'NotFound' })
    }
  } catch {
    await router.push({ name: 'NotFound' })
  }
})
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding-top: 20px;
}

.button-group {
  display: flex;
  gap: 10px;
  margin-top: 20px;
  justify-content: center;
}
</style>
