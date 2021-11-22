import axios from "axios";
import cookies from "vue-cookies";

// const URL = 'http://localhost:8000/'
const URL = 'http://j5a601.p.ssafy.io:8000/'

const ROUTES = {
  detail: 'artifacts/',
  museum: 'artifacts/museum/',
  today: 'pages/recommend',
  saveResemble(artifactId) {
    return `artifacts/${artifactId}/resemble/`
  },
}

const token = {'Authorization': `Token ${cookies.get('user-token')}`}
const SERVICE_KEY = 'SrLLfGdZjGbS5OmPmSlewYvcR6tXPmpk11SduYlvFr7r6CA7L9vjF7JRSx7rhrTEvOdAlUDtqkY9HJAg8%2BY6ww%3D%3D'

// 오늘의 문화재 요청
async function requestToday() {
  const todayPath = URL + ROUTES.today
  return await axios.get(todayPath)
}

// 유물 상세정보 요청
async function requestDetail(id) {
  const detailPath = URL + ROUTES.detail + id
  return await axios.get(detailPath)
}

// 닮은 유물 저장
async function saveResembleArtifact(artifactId) {
  const saveResemblePath = URL + ROUTES.saveResemble(artifactId)
  console.log(token)
  // data 없이 headers 넘기는 법?
  await axios.post(saveResemblePath, token, {headers: token})
}



const ArtifactsApi = {
  URL,
  ROUTES,
  SERVICE_KEY,
  requestToday: () => requestToday(),
  requestDetail: (id) => requestDetail(id),
  saveResembleArtifact: (artifactId) => saveResembleArtifact(artifactId)
}

export default ArtifactsApi