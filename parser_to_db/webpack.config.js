module.exports = {
    rules: [
        {
            test: /\.(js|jsx|tsx|ts)$/,
            exclude: /node_modules/,
            loader: 'babel-loader'
        }
    ],
    resolve: {
        extensions: ['*', '.js', '.jsx', '.tsx', '.ts'],
    }
}