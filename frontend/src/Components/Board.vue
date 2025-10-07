<template>
  <div class="board-container">
    <h2>🎮 Tablero</h2>
    
    <div v-if="!board?.success" class="empty-board">
      <p>No hay tablero creado</p>
      <p class="hint">Crea un tablero para empezar</p>
    </div>

    <div v-else class="board-wrapper">
      <div class="board-info">
        <span>Tamaño: {{ board.width }}x{{ board.height }}</span>
        <span>Paredes: {{ board.walls?.length || 0 }}</span>
      </div>

      <div 
        class="board-grid" 
        :style="gridStyle"
      >
        <div
          v-for="cell in cells"
          :key="`${cell.x}-${cell.y}`"
          :class="getCellClass(cell)"
        >
          <span v-if="hasWall(cell)" class="cell-content">🧱</span>
          <img v-else-if="hasRobot(cell)" 
            :src="getRobotImage()" 
            alt="Robot"
            class="cell-content robot-image"
            />
          <span v-else class="cell-coords">{{ cell.x }},{{ cell.y }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  board: Object,
  robot: Object
})

const emit = defineEmits(['refresh'])

const gridStyle = computed(() => {
  if (!props.board?.success) return {}
  return {
    gridTemplateColumns: `repeat(${props.board.width}, 1fr)`
  }
})

const cells = computed(() => {
  if (!props.board?.success) return []
  
  const cellArray = []
  // Iterar de arriba hacia abajo (y=1 arriba, y=height abajo)
  for (let x = props.board.height; x >= 1; x--) {
    for (let y = 1; y <= props.board.width; y++) {
      cellArray.push({ x, y })
    }
  }
  return cellArray
})

const hasWall = (cell) => {
  if (!props.board?.walls) return false
  return props.board.walls.some(w => w[0] === cell.x && w[1] === cell.y)
}

const hasRobot = (cell) => {
  if (!props.robot?.success) return false
  const pos = props.robot.position
  return pos.x === cell.x && pos.y === cell.y
}

const getCellClass = (cell) => {
  const classes = ['cell']
  if (hasWall(cell)) classes.push('wall')
  if (hasRobot(cell)) classes.push('robot')
  return classes.join(' ')
}

const getRobotImage = () => {
  if (!props.robot?.success) return ''
  
  const images = {
    'NORTH': '/robot-north.png',
    'SOUTH': '/robot-south.png',
    'EAST': '/robot-east.png',
    'WEST': '/robot-west.png'
  }
  
  return images[props.robot.position.facing] || '/robot-north.png'
}
</script>

<style scoped>
.board-container {
  width: 100%;
}

h2 {
  margin: 0 0 1.5rem 0;
  color: #2d3748;
}

.empty-board {
  text-align: center;
  padding: 4rem 2rem;
  background: #f7fafc;
  border-radius: 12px;
  color: #718096;
}

.empty-board .hint {
  font-size: 2rem;
  margin-top: 1rem;
}

.board-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.board-info {
  display: flex;
  gap: 2rem;
  padding: 0.75rem 1rem;
  background: #f7fafc;
  border-radius: 8px;
  font-weight: 500;
  color: #4a5568;
}

.board-grid {
  width: 100%;
  display: grid;
  gap: 2px;
  background: #cbd5e0;
  padding: 2px;
  border-radius: 8px;
  max-width: 100%;
  aspect-ratio: 1;
  margin: 0 auto;
}

.cell {
  aspect-ratio: 1;
  background: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  color: #a0aec0;
  transition: all 0.2s;
  position: relative;
  border-radius: 2px;
}

.cell:hover {
  background: #f7fafc;
}

.cell-content {
  font-size: 1.5rem;
}

.cell-coords {
  font-size: 0.65rem;
  color: #cbd5e0;
}

.cell.wall {
  background: #2d3748;
  cursor: not-allowed;
}

.cell.wall:hover {
  background: #2d3748;
}

.cell.robot {
  background: #4299e1;
  animation: pulse 2s infinite;
}

.robot-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@media (max-width: 768px) {
  .board-grid {
    max-width: 100%;
  }
  
  .cell-content {
    font-size: 1.2rem;
  }
  
  .cell.robot .cell-content {
    font-size: 1.5rem;
  }
}
</style>