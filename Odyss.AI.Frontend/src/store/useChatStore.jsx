import {create} from "zustand"
//der Name ist frei wählbar, wie wenn ich eine funktion deklariere
const useChatStore = create((set)=>({
    messages: [], // hier deklariere ich ein leeres Array
    addMessage:(message) =>
        set((state)=>({messages:[...state.messages,message]})),
}))
export default useChatStore;