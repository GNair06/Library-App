<template>
    <div style="padding: 10px;">
        <h2>All Users</h2><br>
        <table style="margin: auto;">
            <tr>
                <th style="padding: 10px;">Email</th>
                <th style="padding: 10px;">Name</th>
                <th style="padding: 10px;">Role</th>
            </tr>

            <tr v-for="user in all_users" :key="user.id">
                <td style="padding: 10px;">{{ user.email }}</td>
                <td style="padding: 10px;">{{ user.name }}</td>
                <td style="padding: 10px;">{{ user.role }}</td>
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
        this.getAllUsers();
    },
    methods: {
        getAllUsers(){
            const token = localStorage.getItem("access_token");
            console.log(token);
            fetch("http://127.0.0.1:5000/view_all_users",{
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