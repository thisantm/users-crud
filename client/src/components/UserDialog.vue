<template>
  <q-dialog
    :model-value="visible"
    @update:model-value="updateVisible"
  >
    <q-card class="user-card">
      <q-card-section>
        <div class="text-h6">{{ user ? 'Edit User' : 'Create User' }}</div>
      </q-card-section>
      <q-card-section>
        <q-input
          v-model="form.username"
          label="Username"
        />
        <q-select
          v-model="form.roles"
          label="Roles"
          :options="roleOptions"
          multiple
          emit-value
          map-options
        />
        <q-input
          v-model="form.preferences.timezone"
          label="Timezone"
        />
        <q-toggle
          v-model="form.active"
          label="Is Active?"
        />
      </q-card-section>
      <q-card-actions align="right">
        <q-btn
          flat
          label="Cancel"
          @click="closeDialog"
        />
        <q-btn
          flat
          label="Submit"
          @click="submitForm"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue'
import type { User } from 'components/models'

const props = defineProps<{ visible: boolean; user: User | null }>()
const emit = defineEmits(['update:visible', 'submit'])

const form = ref<User>({
  _id: '',
  username: '',
  roles: [],
  preferences: { timezone: '' },
  active: false,
  created_ts: new Date()
})

const roleOptions = [
  { label: 'Admin', value: 'admin' },
  { label: 'Manager', value: 'manager' },
  { label: 'Tester', value: 'tester' }
]

watch(
  () => props.user,
  (newUser) => {
    if (newUser) {
      form.value = { ...newUser, roles: newUser.roles }
    } else {
      form.value = {
        _id: '',
        username: '',
        roles: [],
        preferences: { timezone: '' },
        active: false,
        created_ts: new Date()
      }
    }
  },
  { immediate: true }
)

const submitForm = () => {
  emit('submit', { ...form.value })
  emit('update:visible', false)
}

const closeDialog = () => {
  emit('update:visible', false)
}

const updateVisible = (value: boolean) => {
  emit('update:visible', value)
}
</script>

<style scoped>
.user-card {
  width: 40%;
  height: 40%;
}
</style>
