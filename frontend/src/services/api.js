import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  // ==================== BOARD ====================
  
  async createBoard(width, height) {
    const response = await api.post('/board', { width, height })
    return response.data
  },

  async getBoard() {
    const response = await api.get('/board')
    return response.data
  },

  async deleteBoard() {
    const response = await api.delete('/board')
    return response.data
  },

  async addWall(x, y) {
    const response = await api.post('/board/wall', { x, y })
    return response.data
  },

  // ==================== ROBOT ====================
  
  async placeRobot(x, y, facing) {
    console.log(facing)
    const response = await api.post('/robot/place', { x, y, facing })
    return response.data
  },

  async moveRobot() {
    const response = await api.post('/robot/move')
    return response.data
  },

  async turnLeft() {
    const response = await api.post('/robot/left')
    return response.data
  },

  async turnRight() {
    const response = await api.post('/robot/right')
    return response.data
  },

  async getRobotReport() {
    const response = await api.get('/robot/report')
    return response.data
  },

  async deleteRobot() {
    const response = await api.delete('/robot')
    return response.data
  },

  // ==================== HEALTH ====================
  
  async healthCheck() {
    const response = await api.get('/health')
    return response.data
  }
}