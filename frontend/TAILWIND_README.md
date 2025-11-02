# Configuration Tailwind CSS v4

Ce projet utilise **Tailwind CSS v4** avec Vue 3 et Vite.

## Fichiers de configuration

### 1. `postcss.config.js`
```js
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
}
```

### 2. `tailwind.config.mjs`
```js
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 3. `src/index.css`
```css
@import "tailwindcss";
```

## Différences avec Tailwind v3

Tailwind CSS v4 utilise une syntaxe simplifiée :
- ✅ `@import "tailwindcss";` au lieu de `@tailwind base; @tailwind components; @tailwind utilities;`
- ✅ Plugin PostCSS `@tailwindcss/postcss` au lieu de `tailwindcss` et `autoprefixer`
- ✅ Configuration plus simple dans `tailwind.config.mjs`

## Commandes

```bash
# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm run dev

# Construire pour la production
npm run build
```

## Classes Tailwind utilisées dans l'app

L'application utilise de nombreuses classes Tailwind pour :
- **Gradients** : `bg-gradient-to-br`, `from-blue-400`, `via-indigo-500`
- **Dark Mode** : Classes conditionnelles avec `:class` de Vue
- **Animations** : `transition`, `hover:scale-105`, `duration-200`
- **Responsive** : `flex`, `gap-2`, `p-4`, `rounded-xl`
- **Typographie** : `text-4xl`, `font-extrabold`, `bg-clip-text`

## Résolution des problèmes

Si Tailwind ne fonctionne pas :
1. Vérifiez que `@import "tailwindcss";` est dans `src/index.css`
2. Vérifiez que `postcss.config.js` existe et est correct
3. Vérifiez que le fichier CSS est importé dans `main.js`
4. Redémarrez le serveur de développement
