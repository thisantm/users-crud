<template>
  <q-dialog
    :model-value="visible"
    @update:model-value="updateVisible"
  >
    <q-card>
      <q-card-section>
        <div class="text-h6">Confirm Delete</div>
      </q-card-section>
      <q-card-section> Are you sure you want to delete this user? </q-card-section>
      <q-card-actions align="right">
        <q-btn
          flat
          label="Cancel"
          @click="closeDialog"
        />
        <q-btn
          flat
          label="Delete"
          color="negative"
          @click="confirmDelete"
        />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { defineEmits } from 'vue'

defineProps<{ visible: boolean }>()
const emit = defineEmits(['update:visible', 'confirm'])

const closeDialog = () => {
  emit('update:visible', false)
}

const confirmDelete = () => {
  emit('confirm')
  emit('update:visible', false)
}

const updateVisible = (value: boolean) => {
  emit('update:visible', value)
}
</script>
