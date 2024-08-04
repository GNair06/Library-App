<template>
    <div>
        <table style="margin-left: auto; margin-right: auto; margin-top: 80px;">
            <tr v-for="user in all_users" :key="user.id">
                <td v-if="(user.role == 'admin')">
                    <router-link class="abc" to="/admin_dashboard">Click Here to Get Started!</router-link>
                </td>
                <td v-if="(user.role == 'librarian')">
                    <router-link class="abc" to="/librarian_dashboard">Click Here to Get Started!</router-link>
                </td>
                <td v-if="(user.role == 'user')">
                    <router-link class="abc" to="/user_dashboard">Click Here to Get Started!</router-link>
                </td>
            </tr>
        </table>
    </div>
</template>

<script>
export default{
    data(){
        return {
        all_users: []
    };
    },
    mounted(){
        this.getready();
    },
    methods: {
        getready(){
            const token = localStorage.getItem("access_token");
            console.log(token);
            fetch("http://127.0.0.1:5000/dashboard",{
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem("access_token"),
                },
            })
            .then(resp => {
                console.log(resp);
                return resp.json();
            })
            .then(data => {
                console.log(data);
                this.all_users = data.all_users;
                console.log(this.all_users)
            })
            .catch(error => {
                console.log(error);
            })
        }
    }
    
}
</script>

<style>
.abc{
    text-align: center;
    font-size: 50px;
    padding: 50px;
    margin: 30px;
    background-color: rgb(235, 228, 228);
}
</style>