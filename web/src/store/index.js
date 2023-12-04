import { createStore } from 'vuex'

// 全局变量
const store = createStore({
    state: {
        // 保存选中菜单id
        currentMenu: 1
        },
    mutations: {
        setCurrentMenu (state, payload) {
            state.currentMenu = payload.currentMenu
            console.log('setCurrentMenu:'+ state.currentMenu)

        }
    }
  })
  export default store