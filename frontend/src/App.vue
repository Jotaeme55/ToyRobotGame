<template>
  <div id="app">
    <header>
      <h1>🤖 Robot Game</h1>
      <p class="subtitle">Controla el robot en el tablero</p>
    </header>

    <div class="container">
      <div class="main-content">
        <!-- Tablero -->
        <Board
          :board="boardData"
          :robot="robotData"
          @refresh="loadGameState"
        />
      </div>

      <div class="sidebar">



      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Board from './components/Board.vue'

import api from './services/api.js'


const boardData = ref(null)
const robotData = ref(null)

const loadGameState = async () => {
  try {
    // Cargar board y robot por separado
    await loadBoard()
    await loadRobot()
  } catch (error) {
    console.error('Error al cargar el estado del juego', error)
  }
}

const loadBoard = async () => {
  try {
    const board = await api.getBoard()
    boardData.value = board
  } catch (error) {
    // Si no existe el board, establecer como no exitoso
    boardData.value = { success: false, message: 'No existe un tablero creado' }
  }
}

const loadRobot = async () => {
  try {
    const robot = await api.getRobotReport()
    robotData.value = robot
  } catch (error) {
    // Si no existe el robot, establecer como no exitoso
    robotData.value = { success: false, message: 'El robot no ha sido colocado' }
  }
}

onMounted(() => {
  loadGameState()
})
</script>

<style scoped>
header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  margin: 0;
  font-size: 2.5rem;
}

.subtitle {
  margin: 0.5rem 0 0 0;
  opacity: 0.9;
}

.container {
  max-width: 1400px;
  margin: 2rem auto;
  padding: 0 1rem;
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 2rem;
}

.main-content {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

@media (max-width: 1024px) {
  .container {
    grid-template-columns: 1fr;
  }
}
</style>
