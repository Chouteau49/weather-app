<template>
  <div :class="['min-h-screen flex items-center justify-center transition-colors duration-500 p-4', 
               darkMode ? 'bg-gradient-to-br from-gray-900 via-gray-800 to-gray-700' : 'bg-gradient-to-br from-blue-400 via-indigo-500 to-purple-600']">
    <div :class="['max-w-lg w-full p-8 rounded-2xl shadow-2xl backdrop-blur-lg', 
                  darkMode ? 'bg-gray-900/80' : 'bg-white/80']">
      
      <!-- En-tête avec bouton mode sombre -->
      <div class="flex justify-between items-center mb-8">
        <h1 :class="['text-4xl font-extrabold bg-clip-text text-transparent drop-shadow-lg', 
                     darkMode ? 'bg-gradient-to-r from-yellow-400 via-pink-400 to-purple-600' : 'bg-gradient-to-r from-blue-600 via-indigo-500 to-purple-600']">
          🌦️ Météo App
        </h1>
        <button @click="toggleDark" 
                :class="['px-3 py-2 rounded-full shadow transition', 
                         darkMode ? 'bg-yellow-400 text-gray-900 hover:bg-yellow-300' : 'bg-gray-800 text-white hover:bg-gray-700']">
          {{ darkMode ? '☀️' : '🌙' }}
        </button>
      </div>

      <!-- Formulaire de recherche -->
      <div class="flex gap-2 mb-8">
        <input 
          v-model="city" 
          @keyup.enter="fetchWeather" 
          placeholder="Entrez une ville (ex: Paris)"
          :class="['flex-1 px-4 py-3 border-2 rounded-xl focus:outline-none focus:ring-4 text-lg shadow-sm transition', 
                   darkMode ? 'border-gray-700 bg-gray-800 text-white placeholder:text-gray-400 focus:ring-yellow-400' : 'border-indigo-300 bg-white text-gray-900 placeholder:text-gray-400 focus:ring-indigo-400']" 
        />
        <button 
          @click="fetchWeather"
          :class="['px-6 py-3 font-bold rounded-xl shadow-lg hover:scale-105 transition-transform duration-200', 
                   darkMode ? 'bg-gradient-to-r from-yellow-400 to-pink-400 text-gray-900 hover:from-yellow-300 hover:to-pink-300' : 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700']">
          Rechercher
        </button>
      </div>

      <!-- Affichage de la météo -->
      <transition name="fade">
        <div v-if="weather" 
             :class="['p-6 rounded-2xl shadow-lg flex flex-col items-center mb-6', 
                      darkMode ? 'bg-gradient-to-br from-gray-800 via-gray-700 to-gray-900' : 'bg-gradient-to-br from-blue-100 via-indigo-100 to-purple-100']">
          
          <!-- Icône météo SVG -->
          <svg v-if="icon" 
               :class="'w-20 h-20 mb-4 drop-shadow-lg ' + icon.color" 
               fill="none" 
               viewBox="0 0 64 64" 
               xmlns="http://www.w3.org/2000/svg">
            <circle cx="32" cy="32" r="28" :fill="icon.bg" />
            <path :d="icon.path" 
                  :stroke="icon.color" 
                  stroke-width="3" 
                  stroke-linecap="round" 
                  stroke-linejoin="round" />
          </svg>

          <h2 :class="['text-2xl font-bold mb-2', darkMode ? 'text-yellow-400' : 'text-indigo-700']">
            {{ weather.city }}
          </h2>
          <p :class="['text-5xl font-extrabold mb-2', darkMode ? 'text-pink-400' : 'text-blue-600']">
            {{ weather.temperature }}°C
          </p>
          <p :class="['text-lg italic mb-4', darkMode ? 'text-gray-200' : 'text-gray-700']">
            {{ weather.description }}
          </p>

          <!-- Informations supplémentaires -->
          <div :class="['text-sm mt-2', darkMode ? 'text-gray-300' : 'text-gray-600']">
            <span class="mr-3">💧 Humidité: {{ weather.humidity || 'N/A' }}%</span>
            <span>💨 Vent: {{ weather.windSpeed || 'N/A' }} km/h</span>
          </div>
        </div>
      </transition>

      <!-- Message d'erreur -->
      <transition name="fade">
        <p v-if="error" 
           :class="['font-semibold text-center p-3 rounded-lg', 
                    darkMode ? 'text-pink-400 bg-red-900/50' : 'text-red-600 bg-red-100 border border-red-300']">
          {{ error }}
        </p>
      </transition>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// Définitions des icônes SVG basées sur la description météo
const icons = [
  {
    match: /rain|shower|pluie|drizzle/i,
    path: 'M32 44v6M24 44v6M40 44v6M20 36a12 12 0 0224 0c0 6.627-5.373 12-12 12s-12-5.373-12-12z',
    color: 'text-blue-500',
    bg: '#a5b4fc',
  },
  {
    match: /cloud|nuage|overcast|gris/i,
    path: 'M20 36a12 12 0 0224 0c0 6.627-5.373 12-12 12s-12-5.373-12-12z',
    color: 'text-gray-400',
    bg: '#e0e7ff',
  },
  {
    match: /sun|soleil|clear|ensoleillé|ciel clair/i,
    path: 'M32 20v-6M32 50v-6M44 32h6M14 32h6M24.22 24.22l-4.24-4.24M43.78 43.78l4.24 4.24M43.78 24.22l4.24-4.24M24.22 43.78l-4.24 4.24M32 32a12 12 0 100-24 12 12 0 000 24z',
    color: 'text-yellow-400',
    bg: '#fde68a',
  },
  {
    match: /snow|neige|flocons/i,
    path: 'M32 44v6M24 44v6M40 44v6M32 32a12 12 0 100-24 12 12 0 000 24z',
    color: 'text-blue-200',
    bg: '#f0f9ff',
  },
  {
    match: /thunderstorm|orage/i,
    path: 'M32 20v-6M32 50v-6M44 32h6M14 32h6M24.22 24.22l-4.24-4.24M43.78 43.78l4.24 4.24M43.78 24.22l4.24-4.24M24.22 43.78l-4.24 4.24M32 32a12 12 0 100-24 12 12 0 000 24zM32 40l-8 8h16l-8-8z',
    color: 'text-yellow-600',
    bg: '#fcd34d',
  },
]

const city = ref('')
const weather = ref(null)
const error = ref('')
const darkMode = ref(false)

async function fetchWeather() {
  if (!city.value.trim()) {
    error.value = 'Veuillez entrer le nom d\'une ville.'
    return
  }
  
  try {
    const response = await fetch(`/api/weather/${encodeURIComponent(city.value.trim())}`)
    if (response.ok) {
      weather.value = await response.json()
      error.value = ''
    } else {
      error.value = 'Ville non trouvée ou erreur serveur.'
      weather.value = null
    }
  } catch (err) {
    console.error("Erreur de récupération de la météo:", err)
    error.value = 'Erreur réseau lors de la connexion au serveur.'
    weather.value = null
  }
}

const icon = computed(() => {
  if (!weather.value) return null
  const desc = weather.value.description || ''
  const found = icons.find(i => i.match.test(desc))
  return found || icons[1] // Par défaut: nuage
})

function toggleDark() {
  darkMode.value = !darkMode.value
  if (darkMode.value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
