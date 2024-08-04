<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <router-link class="navbar-brand" to="/">Library</router-link>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
                aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavDropdown">
                <ul class="navbar-nav">
                    <li v-if="!this.flag" class="nav-item">
                        <router-link class="nav-link" to="/login">Login</router-link>
                    </li>
                    <li v-if="!this.flag" class="nav-item">
                        <a class="nav-link" href="/#/register">Register</a>
                    </li>
                    <li v-if="this.flag" class="nav-item">
                        <a class="nav-link" href="/#/dashboard">Dashboard</a>
                    </li>
                    <li v-if="this.flag" class="nav-item">
                        <a @click="logout" class="nav-link">Logout</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <br>
</template>
<script>
import UserMixin from '../mixins_folder/UserMixin'
export default {
    mixins: [UserMixin]
}

</script>