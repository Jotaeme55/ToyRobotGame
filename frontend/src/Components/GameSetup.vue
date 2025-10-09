<template>
  <div class="game-setup">
    <h3>Configuración</h3>

    <!-- Crear Tablero -->
    <div class="section">
      <h4>1. Crear Tablero</h4>
      <div class="input-group">
        <input
          v-model.number="boardWidth"
          type="number"
          placeholder="Ancho"
          min="3"
          max="10"
        />
        <input
          v-model.number="boardHeight"
          type="number"
          placeholder="Alto"
          min="3"
          max="10"
        />
      </div>
      <button
        @click="createBoard"
        :disabled="loading || !isValidBoardSize"
        class="btn-primary"
      >
        {{ boardExists ? 'Recrear' : 'Crear' }} Tablero
      </button>
    </div>

    <!-- Añadir Pared -->
    <div v-if="boardExists" class="section">
      <h4>2. Añadir Pared</h4>
      <div class="input-group">
        <input
          v-model.number="wallX"
          type="number"
          placeholder="X"
          min="1"
          class="input-number"
        />
        <input
          v-model.number="wallY"
          type="number"
          placeholder="Y"
          min="1"
          class="input-number"
        />
      </div>
      <button
        @click="addWall"
        :disabled="loading || !isValidWallPosition"
        class="btn-secondary"
      >
        🧱 Añadir Pared
      </button>
    </div>

    <!-- Reset -->
    <div class="section">
      <button
        @click="resetGame"
        :disabled="loading"
        class="btn-danger"
      >
        🔄 Reiniciar Juego
      </button>
    </div>

    <!-- Feedback -->
    <div v-if="feedback.message" :class="['feedback', feedback.type]">
      {{ feedback.message }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '../services/api.js'

const props = defineProps({
  boardExists: Boolean
})

const emit = defineEmits(['board-created', 'wall-added', 'game-reset'])

const boardWidth = ref(5)
const boardHeight = ref(5)
const wallX = ref(null)
const wallY = ref(null)
const loading = ref(false)
const feedback = ref({ message: '', type: 'info' })

const isValidBoardSize = computed(() => {
  return boardWidth.value >= 3 && boardWidth.value <= 10 &&
         boardHeight.value >= 3 && boardHeight.value <= 10
})

const isValidWallPosition = computed(() => {
  return wallX.value >= 1 && wallY.value >= 1
})

const createBoard = async () => {
  if (!isValidBoardSize.value) {
    showFeedback('Tamaño inválido (3-10)', 'error')
    return
  }

  loading.value = true
  try {
    const result = await api.createBoard(boardWidth.value, boardHeight.value)
    if (result.success) {
      showFeedback(result.message, 'success')
      emit('board-created')
    } else {
      showFeedback(result.message, 'error')
    }
  } catch (error) {
    showFeedback(error.response?.data?.message || 'Error al crear tablero', 'error')
  } finally {
    loading.value = false
  }
}

const addWall = async () => {
  if (!isValidWallPosition.value) {
    showFeedback('Posición inválida', 'error')
    return
  }

  loading.value = true
  try {
    console.log(wallX.value,wallY.value)
    const result = await api.addWall(wallX.value, wallY.value)
    if (result.success) {
      showFeedback(result.message, 'success')
      emit('wall-added')
      // Limpiar inputs
      wallX.value = null
      wallY.value = null
    } else {
      showFeedback(result.message, 'error')
    }
  } catch (error) {
    showFeedback(error.response?.data?.message || 'Error al añadir pared', 'error')
  } finally {
    loading.value = false
  }
}

const resetGame = async () => {
  if (!confirm('¿Seguro que quieres reiniciar el juego?')) return

  loading.value = true
  try {
    // Eliminar board y robot por separado
    await api.deleteBoard()
    await api.deleteRobot()
    
    showFeedback('Juego reiniciado exitosamente', 'success')
    emit('game-reset')
  } catch (error) {
    showFeedback(error.response?.data?.message || 'Error al reiniciar', 'error')
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
.game-setup {
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

.input-group {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

input {
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

input:focus {
  outline: none;
  border-color: #667eea;
}

button {
  width: 100%;
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
}

.btn-primary:hover:not(:disabled) {
  background: #5568d3;
  transform: translateY(-1px);
}

.btn-secondary {
  background: #48bb78;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background: #38a169;
  transform: translateY(-1px);
}

.btn-danger {
  background: #f56565;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #e53e3e;
  transform: translateY(-1px);
}

.feedback {
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 500;
  text-align: center;
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
</style>