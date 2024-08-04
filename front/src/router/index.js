import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterPage from '@/views/RegisterPage.vue'
import  LoginPage from '@/views/LoginPage.vue'
import AllUsers from '@/views/AllUsers.vue'
import CreateSection from '@/views/CreateSection.vue'
import AllSections from '@/views/AllSections.vue'
import AddBooks from '@/views/AddBooks.vue'
import DashBoard from '@/views/DashBoard.vue'
import LibDashboard from '@/views/LibDashboard.vue'
import UserDashboard from '@/views/UserDashboard.vue'
import AdminDashboard from '@/views/AdminDashboard.vue'
import EditSection from '@/views/EditSection.vue'
import AllBooks from '@/views/AllBooks.vue'
import AllRequests from '@/views/AllRequests.vue'
import AllIssues from '@/views/AllIssues.vue'
import MyBooks from '@/views/MyBooks.vue'
import ViewContent from '@/views/ViewContent.vue'
import MyRequests from '@/views/MyRequests.vue'
import EditBook from '@/views/EditBook.vue'
import BooksOfSection from '@/views/BooksOfSection.vue'
import SearchSection from '@/views/SearchSection.vue'
import Stats from '@/views/Stats.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },

  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },

  {
    path: '/statistics',
    name: 'statistics',
    component: Stats
  },

  {
    path: '/view_all_users',
    name: 'view_all_users',
    component: AllUsers
  },

  {
    path: '/view_all_requests',
    name: 'view_all_requests',
    component: AllRequests
  },

  {
    path: '/view_all_issues',
    name: 'view_all_issues',
    component: AllIssues
  },

  {
    path: '/view_my_issues',
    name: 'view_my_issues',
    component: MyBooks
  },

  {
    path: '/view_my_requests',
    name: 'view_my_requests',
    component: MyRequests
  },

  {
    path: '/view_all_sections',
    name: 'view_all_sections',
    component: AllSections
  },

  {
    path: '/view_all_books',
    name: 'view_all_books',
    component: AllBooks
  },

  {
    path: '/books_of_section/:id',
    name: 'books_of_section',
    component: BooksOfSection
  },

  {
    path: '/section_form',
    name: 'section_form',
    component: SearchSection
  },

  {
    path: '/view_book_content/:id',
    name: 'view_book_content',
    component: ViewContent
  },

  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },

  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashBoard
  },

  {
    path: '/librarian_dashboard',
    name: 'librarian_dashboard',
    component: LibDashboard
  },

  {
    path: '/admin_dashboard',
    name: 'admin_dashboard',
    component: AdminDashboard
  },

  {
    path: '/user_dashboard',
    name: 'user_dashboard',
    component: UserDashboard
  },

  {
    path: '/create_section',
    name: 'create_section',
    component: CreateSection
  },
  {
    path: '/edit_section/:id',
    name: 'edit_section',
    component: EditSection
  },

  {
    path: '/edit_book/:id',
    name: 'edit_book',
    component: EditBook
  },

  {
    path: '/:id/add_book',
    name: 'add_book',
    component: AddBooks
  },

  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
