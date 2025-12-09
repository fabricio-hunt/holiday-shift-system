import axios from 'axios'


const api = axios.create({
    baseURL: '/api'
})

// Lazy load store to avoid circular dependency
let authStore = null

api.interceptors.request.use(async (config) => {
    if (!authStore) {
        const { useAuthStore } = await import('../stores/auth')
        authStore = useAuthStore()
    }

    if (authStore.authHeader) {
        config.headers.Authorization = authStore.authHeader
    }
    return config
})

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (!authStore) {
            const { useAuthStore } = await import('../stores/auth')
            authStore = useAuthStore()
        }

        if (error.response && error.response.status === 401) {
            authStore.logout()
        }
        return Promise.reject(error)
    }
)

export default api
