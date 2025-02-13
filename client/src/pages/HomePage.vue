<template>
  <q-page class="row justify-evenly q-pa-md">
    <div class="container">
      <div class="button-container">
        <q-btn
          label="Create User"
          color="primary"
          class="fixed-size-btn"
          @click="openUserDialog()"
        />
      </div>
      <q-table
        class="full-width"
        :rows="users"
        :columns="columns"
        row-key="username"
        virtual-scroll
        :virtual-scroll-item-size="50"
        :rows-per-page-options="[10, 25, 50, 0]"
        :rows-per-page="10"
        style="max-height: calc(100vh - 150px)"
      >
        <template v-slot:body-cell-username="props">
          <q-td :props="props">
            <span
              @click="goToUserPage(props.row._id)"
              class="username-link"
            >
              {{ props.row.username }}
            </span>
          </q-td>
        </template>
        <template v-slot:body-cell-actions="props">
          <q-td :props="props">
            <q-btn
              flat
              icon="edit"
              @click="openUserDialog(props.row)"
            />
            <q-btn
              flat
              icon="delete"
              color="negative"
              @click="confirmDeleteUser(props.row._id)"
            />
          </q-td>
        </template>
      </q-table>
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
  </q-page>
</template>

<script setup lang="ts">
import { onBeforeMount, ref } from 'vue'
import { useRouter } from 'vue-router'
import type { User } from 'components/models'
import usersStore from 'src/stores/users-store'
import type { QTableColumn } from 'quasar'
import UserDialog from 'src/components/UserDialog.vue'
import DeleteDialog from 'src/components/DeleteDialog.vue'

const usersStoreCalls = usersStore()
const router = useRouter()

const users = ref<User[]>([])

const columns: QTableColumn<User>[] = [
  {
    name: 'username',
    label: 'Username',
    align: 'center',
    field: 'username',
    style: 'width: 150px'
  },
  {
    name: 'roles',
    label: 'Roles',
    align: 'center',
    field: (row: User) => row.roles.join(', '),
    style: 'width: 200px'
  },
  {
    name: 'timezone',
    label: 'Timezone',
    align: 'center',
    field: (row: User) => row.preferences.timezone,
    style: 'width: 150px'
  },
  {
    name: 'active',
    label: 'Is Active?',
    align: 'center',
    field: 'active',
    style: 'width: 100px'
  },
  {
    name: 'created_ts',
    label: 'Created At',
    align: 'center',
    field: 'created_ts',
    style: 'width: 150px'
  },
  {
    name: 'actions',
    label: 'Actions',
    align: 'center',
    field: '_id',
    style: 'width: 100px'
  }
]

const goToUserPage = async (userId: string) => {
  await router.push({ name: 'UserPage', params: { id: userId } })
}

const isUserDialogVisible = ref(false)
const selectedUser = ref<User | null>(null)

const openUserDialog = (user: User | null = null) => {
  selectedUser.value = user
  isUserDialogVisible.value = true
}

const handleUserSubmit = async (userData: User) => {
  if (selectedUser.value) {
    await usersStoreCalls.updateUser(userData)
    console.log('Editing user:', userData)
  } else {
    await usersStoreCalls.createUser(userData)
    console.log('Creating user:', userData)
  }
  isUserDialogVisible.value = false
  users.value = (await usersStoreCalls.fetchUsers()) as User[]
}

const isDeleteDialogVisible = ref(false)
const userIdToDelete = ref<string | null>(null)

const confirmDeleteUser = (userId: string) => {
  userIdToDelete.value = userId
  isDeleteDialogVisible.value = true
}

const deleteUser = async () => {
  if (userIdToDelete.value) {
    await usersStoreCalls.deleteUser(userIdToDelete.value)
    users.value = (await usersStoreCalls.fetchUsers()) as User[]
    userIdToDelete.value = null
    isDeleteDialogVisible.value = false
  }
}

onBeforeMount(async () => {
  users.value = (await usersStoreCalls.fetchUsers()) as User[]
})
</script>

<style scoped>
.full-width {
  width: 100%;
}

.full-height {
  height: 100%;
}

.username-link {
  color: blue;
  text-decoration: underline;
  cursor: pointer;
}

.fixed-size-btn {
  width: 150px;
  height: 50px;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.button-container {
  align-self: flex-end;
  margin-bottom: 10px;
}
</style>
