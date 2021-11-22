import Vue from 'vue'
import store from '@/store'
import VueRouter from 'vue-router'
import cookies from "vue-cookies";
import Home from '../views/common/Home.vue'
import MainPage from "@/views/common/MainPage";
import SearchPage from '../views/artifacts/SearchPage.vue'
import ProfilePage from "../views/accounts/ProfilePage";
import ProfileLikePage from "@/views/accounts/ProfileLikePage";
import ProfileResemblePage from "@/views/accounts/ProfileResemblePage";
import DetailPage from '@/views/artifacts/DetailPage.vue'
import SearchIndexPage from '@/views/artifacts/SearchIndexPage.vue'
import SearchFilterPage from '@/views/artifacts/SearchFilterPage.vue'
import LoadingPage from '../views/common/LoadingPage.vue'
import ResultPage from "@/views/artifacts/ResultPage";
import LoginPage from "@/views/accounts/LoginPage";
import SignupPage from "@/views/accounts/SignupPage";
import SignInUpPage from "@/views/accounts/SignInUpPage";
import IntroPage from '../views/common/IntroPage.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/main',
    name: 'MainPage',
    component: MainPage
  },
  {
    path: '/intro',
    name: 'IntroPage',
    component: IntroPage
  },
  {
    path: '/search',
    component: SearchPage,
    children: [
      {path: '', name: 'SearchIndexPage', component: SearchIndexPage},
      {path: 'filter', name: 'SearchFilterPage', component: SearchFilterPage},
    ]
  },
  {
    path: '/profile',
    component: ProfilePage,
    children: [
      {path: '', name: 'ProfileLikePage', component: ProfileLikePage},
      {path: 'resemble', name: 'ProfileResemblePage', component: ProfileResemblePage}
    ]
  },

  // 로그인/ 회원가입
  {
    path: '/login', component: SignInUpPage,
    children: [
        {path: '', name: 'LoginPage', component: LoginPage},
        // 회원가입
        {path: '/signup', name: 'SignupPage', component: SignupPage},
      ]
  },
  {
    path: '/loading',
    name: 'LoadingPage',
    component: LoadingPage,
  },
  {
    path: '/detail/:artifactId',
    name: 'DetailPage',
    component: DetailPage,
  },
  {
    path: '/result',
    name: 'ResultPage',
    component: ResultPage
  }

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})


export default router
