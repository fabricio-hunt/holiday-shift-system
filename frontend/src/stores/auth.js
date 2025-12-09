import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api' // Circular dep handling? api imports this.
// To avoid circular dependency, we can inject token differently or just use the store in interceptor (lazy).
// The api.js imports useAuthStore, which is fine as long as we don't use api inside the store definition synchronously?

export const useAuthStore = defineStore('auth', () => {
    const user = ref(JSON.parse(localStorage.getItem('user')) || null)
    const authHeader = ref(localStorage.getItem('authHeader') || null)

    const isAuthenticated = computed(() => !!user.value && !!authHeader.value)

    const router = useRouter()

    function login(email, password) {
        // Basic Auth Header
        const token = btoa(`${email}:${password}`)
        const header = `Basic ${token}`

        // Optimistically set state or verify with a request (preferred)
        // We'll verify by hitting an endpoint that requires auth, e.g. /shifts or a specific /me if it existed.
        // For now, let's try to list shifts. If we get 401, it fails.

        // Storing temporarily to attempt request
        authHeader.value = header

        return api.get('/shifts')
            .then(() => {
                // Success
                user.value = { email }
                authHeader.value = header

                localStorage.setItem('user', JSON.stringify(user.value))
                localStorage.setItem('authHeader', authHeader.value)
                return true
            })
            .catch((err) => {
                authHeader.value = null
                user.value = null
                throw err
            })
    }

    function logout() {
        user.value = null
        authHeader.value = null
        localStorage.removeItem('user')
        localStorage.removeItem('authHeader')
        // We need to access router from component or inject it? router is undefined here usually.
        // We'll reload or let the component handle redirect.
        window.location.href = '/login'
    }

    return { user, authHeader, isAuthenticated, login, logout }
})
