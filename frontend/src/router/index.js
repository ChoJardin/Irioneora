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
  // {
  //   path: '/',
  //   name: 'Home',
  //   component: Home,
  //   meta: {
  //     enterActiveClass: "animate__animated animate__fadeIn animate__slow",
  //     leaveActiveClass: "animate__animated animate__fadeOut animate__slow"
  //   },
  // },
  {
    path: '/',
    name: 'MainPage',
    component: MainPage,
    meta: {
      enterActiveClass: "animate__animated animate__fadeIn animate__fast",
      leaveActiveClass: "animate__animated animate__fadeOut animate__fast"
    },
  },
  // {
  //   path: '/intro',
  //   name: 'IntroPage',
  //   component: IntroPage,
  //   meta: {
  //     enterActiveClass: "animate__animated animate__fadeIn animate__fast",
  //     leaveActiveClass: "animate__animated animate__fadeOut animate__slow"
  //   },
  // },
  {
    path: '/search',
    component: SearchPage,
    children: [
      {
        path: '', name: 'SearchIndexPage', component: SearchIndexPage,
        meta: {
          enterActiveClass: "animate__animated animate__fadeIn",
          leaveActiveClass: ""
        }
      },
      {
        path: 'filter', name: 'SearchFilterPage', component: SearchFilterPage,
        meta: {
          enterActiveClass: "animate__animated animate__fadeIn",
          leaveActiveClass: ""
        }
      },
    ],
  },
  {
    path: '/profile',
    component: ProfilePage,
    children: [
      {
        path: '', name: 'ProfileLikePage', component: ProfileLikePage,
        meta: {
          enterActiveClass: "animate__animated animate__fadeIn",
          leaveActiveClass: ""
        }
      },
      {
        path: 'resemble', name: 'ProfileResemblePage', component: ProfileResemblePage,
        meta: {
          enterActiveClass: "animate__animated animate__fadeIn",
          leaveActiveClass: ""
        }
      }
    ],
  },

  // 로그인/ 회원가입
  {
    path: '/login', component: SignInUpPage,
    children: [
        {
          path: '', name: 'LoginPage', component: LoginPage,
          meta: {
            enterActiveClass: "animate__animated animate__fadeIn",
            leaveActiveClass: ""
          }
        },
        // 회원가입
        {
          path: '/signup', name: 'SignupPage', component: SignupPage,
          meta: {
            enterActiveClass: "animate__animated animate__fadeIn",
            leaveActiveClass: ""
          }
        },
    ],
  },
  {
    path: '/loading',
    name: 'LoadingPage',
    component: LoadingPage,
    meta: {
      enterActiveClass: "animate__animated animate__fadeIn",
      leaveActiveClass: "animate__animated animate__fadeOut"
    },
  },
  {
    path: '/detail/:artifactId',
    name: 'DetailPage',
    component: DetailPage,
    meta: {
      enterActiveClass: "animate__animated animate__fadeIn__fast",
      leaveActiveClass: "animate__animated animate__fadeOut"
    },
  },
  {
    path: '/result',
    name: 'ResultPage',
    component: ResultPage,
    meta: {
      enterActiveClass: "animate__animated animate__fadeIn__fast",
      leaveActiveClass: "animate__animated animate__fadeOut"
    },
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// navigation guard
router.beforeEach((to, from, next) => {
  // 결과 페이지
  if (to.name === 'ResultPage') {
    if (store.getters.isResult) {
      next()
    } else next('/')
  }

  // 로그인
  if (to.path === '/login' || to.path === '/signup') {
    if (store.getters.isLoggedIn) {
      next('/profile')
    }
  }

  next()
})

export default router
