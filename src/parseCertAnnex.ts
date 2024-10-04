import XLSX from 'xlsx'
import cities from './reference-data/cities.json'
import { City } from './types'

export default function parseCertAnnex(filePath: string): {
    city: string
    purpose: string
} {
    // Книга
    const workbook = XLSX.readFile(filePath)

    // Аркуші
    const generalBuildingInfo = workbook.Sheets['1.1']

    const extractCityFromAddress = (address: string): string => {
        const lowerCaseAddress = address.toLowerCase()

        for (const city of cities as City[]) {
            const lowerCaseCityUa = city.cityUa.toLowerCase()

            if (lowerCaseAddress.includes(lowerCaseCityUa)) {
                return city.city
            }
        }
        throw new Error(`Місто не знайдено в рядку: "${address}"`)
    }

    const inputData = {
        // 1.1 Загальна інформація про будівлю
        city: extractCityFromAddress(generalBuildingInfo['D3'].v),
        purpose: generalBuildingInfo['D4'].v,
    }

    return inputData
}
