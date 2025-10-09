<template>
  <div class="robot-controls">
    <h3>🤖 Control del Robot</h3>

    <!-- Colocar Robot -->
    <div class="section">
      <h4>{{ robotPlaced ? '📍 Reposicionar' : '1. Colocar Robot' }}</h4>
      <div class="input-row">
        <input
          v-model.number="placeX"
          type="number"
          placeholder="X"
          min="1"
          :disabled="!boardExists"
          class="input-number"
        />
        <input
          v-model.number="placeY"
          type="number"
          placeholder="Y"
          min="1"
          :disabled="!boardExists"
          class="input-number"
        />
      </div>
      <select
        v-model="placeFacing"
        :disabled="!boardExists"
      >
        <option value="NORTH">Norte ⬆️</option>
        <option value="SOUTH">Sur ⬇️</option>
        <option value="EAST">Este ➡️</option>
        <option value="WEST">Oeste ⬅️</option>
      </select>
      <button
        @click="placeRobot"
        :disabled="loading || !boardExists || !isValidPlacePosition"
        class="btn-primary"
      >
        {{ robotPlaced ? '📍 Reposicionar' : '🚀 Colocar' }} Robot
      </button>
    </div>

    <!-- Controles de Movimiento -->
    <div v-if="robotPlaced" class="section">
      <h4>2. Mover Robot</h4>
      
      <div class="movement-grid">
        <div></div>
        <button
          @click="turnLeft"
          :disabled="loading"
          class="btn-control"
        >
          ⬅️ Izq
        </button>
        <div></div>
        
        <button
          @click="moveRobot"
          :disabled="loading"
          class="btn-control btn-move"
        >
          ⬆️ Mover
        </button>
        
        <button
          @click="getReport"
          :disabled="loading"
          class="btn-control btn-report"
        >
          📍 Posición
        </button>
        
        <button
          @click="turnRight"
          :disabled="loading"
          class="btn-control"
        >
          Dch ➡️
        </button>
      </div>
    </div>

    <!-- Feedback -->
    <div v-if="feedback.message" :class="['feedback', feedback.type]">
      {{ feedback.message }}
    </div>

    <!-- Hint -->
    <div v-if="!boardExists" class="hint">
      ⚠️ Primero crea un tablero
    </div>
    <div v-else-if="!robotPlaced" class="hint">
      💡 Coloca el robot para empezar a jugar
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '../services/api.js'

const props = defineProps({
  robotPlaced: Boolean,
  boardExists: Boolean
})

const emit = defineEmits(['robot-action'])

const placeX = ref(1)
const placeY = ref(1)
const placeFacing = ref('NORTH')
const loading = ref(false)
const feedback = ref({ message: '', type: 'info' })

const isValidPlacePosition = computed(() => {
  return placeX.value >= 1 && placeY.value >= 1 && placeFacing.value
})

const placeRobot = async () => {
  if (!isValidPlacePosition.value) {
    showFeedback('Posición inválida', 'error')
    return
  }

  loading.value = true
  try {
    const result = await api.placeRobot(placeX.value, placeY.value, placeFacing.value)
    if (result.success) {
      showFeedback(result.message, 'success')
      emit('robot-action')
    } else {
      showFeedback(result.message, 'error')
    }
  } catch (error) {
    showFeedback(error.response?.data?.message || 'Error al colocar robot', 'error')
  } finally {
    loading.value = false
  }
}

const moveRobot = async () => {
  loading.value = true
  try {
    const result = await api.moveRobot()
    if (result.success) {
      showFeedback(result.message, 'success')
      emit('robot-action')
    } else {
      showFeedback(result.message, 'error')
    }
  } catch (error) {
    showFeedback(error.response?.data?.message || 'Error al mover robot', 'error')
  } finally {
    loading.value = false
  }
}

const turnLeft = async () => {
  loading.value = true
  try {
    const result = await api.turnLeft()
    if (result.success) {
      showFeedback(result.message, 'success')
      emit('robot-action')
    } else {
      showFeedback(result.message, 'error')
    }
  } catch (error) {
    showFeedback(error.response?.data?.message || 'Error al girar', 'error')
  } finally {
    loading.value = false
  }
}

const turnRight = async () => {
  loading.value = true
  try {
    const result = await api.turnRight()
    if (result.success) {
      showFeedback(result.message, 'success')
      emit('robot-action')
    } else {
      showFeedback(result.message, 'error')
    }
  } catch (error) {
    showFeedback(error.response?.data?.message || 'Error al girar', 'error')
  } finally {
    loading.value = false
  }
}

const getReport = async () => {
  loading.value = true
  try {
    const result = await api.getRobotReport()
    if (result.success) {
      showFeedback(result.message, 'success')
    } else {
      showFeedback(result.message, 'error')
    }
  } catch (error) {
    showFeedback(error.response?.data?.message || 'Error al obtener posición', 'error')
  } finally {
    loading.value = false
  }
}

const showFeedback = (message, type = 'info') => {
  feedback.value = { message, type }
  setTimeout(() => {
    feedback.value = { message: '', type: 'info' }
  }, 3000)
}
</script>

<style scoped>
.robot-controls {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

h3 {
  margin: 0 0 1.5rem 0;
  color: #2d3748;
}

.section {
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.section:last-of-type {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

h4 {
  margin: 0 0 0.75rem 0;
  color: #4a5568;
  font-size: 0.9rem;
  font-weight: 600;
}

.input-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

input, select {
  flex: 1;
  padding: 0.75rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.9rem;
  transition: border-color 0.2s;
}
.input-number {
  width: 45%;
}

input:focus, select:focus {
  outline: none;
  border-color: #667eea;
}

select {
  margin-bottom: 0.75rem;
  width: 100%;
}

button {
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background: #667eea;
  color: white;
  width: 100%;
}

.btn-primary:hover:not(:disabled) {
  background: #5568d3;
  transform: translateY(-1px);
}

.movement-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
}

.btn-control {
  background: #4299e1;
  color: white;
  font-size: 0.85rem;
  padding: 0.75rem 0.5rem;
}

.btn-control:hover:not(:disabled) {
  background: #3182ce;
  transform: translateY(-1px);
}

.btn-move {
  background: #48bb78;
}

.btn-move:hover:not(:disabled) {
  background: #38a169;
}

.btn-report {
  background: #ed8936;
}

.btn-report:hover:not(:disabled) {
  background: #dd6b20;
}

.feedback {
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  text-align: center;
  margin-top: 1rem;
}

.feedback.success {
  background: #c6f6d5;
  color: #22543d;
}

.feedback.error {
  background: #fed7d7;
  color: #742a2a;
}

.feedback.info {
  background: #bee3f8;
  color: #2c5282;
}

.hint {
  padding: 0.75rem;
  background: #fef5e7;
  border-left: 4px solid #f6ad55;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #744210;
  margin-top: 1rem;
}
</style>