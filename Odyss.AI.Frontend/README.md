# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

Aufbau meines Projektsverzeichnisses für das bessere Verstädnis

/my-react-app
├── /public
├── /src
│   ├── /assets
│   │   └── /images
│   │   └── /styles
│   ├── /components
│   │   └── /common
│   │   └── /specificComponent
│   ├── /features
│   │   └── /counter
│   │       └── Counter.js
│   │       └── counterStore.js
│   ├── /hooks
│   │   └── useSomeHook.js
│   ├── /pages
│   │   └── HomePage.js
│   │   └── AboutPage.js
│   ├── /store
│   │   └── rootStore.js
│   ├── /utils
│   │   └── api.js
│   │   └── helpers.js
│   ├── App.js
│   ├── index.js
├── .gitignore
├── package.json
├── README.md
