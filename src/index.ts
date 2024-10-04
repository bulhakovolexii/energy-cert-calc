import fs from 'fs'
import path from 'path'
import parseCertAnnex from './parseCertAnnex'

// Отримуємо аргументи командного рядка
const args: string[] = process.argv.slice(2)
if (args.length === 0) {
    console.error(
        'Будь ласка, вкажіть шлях до файлу або директорії з Excel-файлами.'
    )
    process.exit(1)
}

const filePath: string = args[0]

// Перевіряємо, чи існує шлях
if (!fs.existsSync(filePath)) {
    console.error('Шлях не знайдено!')
    process.exit(1)
}

// Функція для обробки Excel-файлів
function processFile(file: string): void {
    const buildingData = parseCertAnnex(file)
    console.log(`Обробка файлу: ${file}`)
    console.log(buildingData)
}

// Перевіряємо, чи це директорія
if (fs.lstatSync(filePath).isDirectory()) {
    // Отримуємо список файлів у директорії
    const files: string[] = fs.readdirSync(filePath)

    // Фільтруємо тільки файли з розширенням .xlsx або .xls
    const excelFiles: string[] = files.filter(
        (file) => file.endsWith('.xlsx') || file.endsWith('.xls')
    )

    if (excelFiles.length === 0) {
        console.error('Не знайдено Excel-файлів у зазначеній директорії.')
        process.exit(1)
    }

    // Обробляємо кожен Excel-файл
    excelFiles.forEach((file) => {
        const fullPath: string = path.join(filePath, file)
        processFile(fullPath)
    })
} else {
    // Якщо передано файл, обробляємо його
    processFile(filePath)
}
