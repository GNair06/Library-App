<template>
    <div>
        <h1 style="background-color: antiquewhite; padding: 10px;">User Dashboard</h1><br>
        <h2 style="background-color: lightpink; padding: 10px;"><router-link :to="`/view_all_sections`">All sections</router-link></h2><br>
        <h2 style="background-color: lightpink; padding: 10px;"><router-link :to="`/view_all_books`">All books</router-link></h2><br>
        <h2 style="background-color: lightpink; padding: 10px;"><router-link :to="`/view_my_issues`">My Books</router-link></h2><br>
        <h2 style="background-color: lightpink; padding: 10px;"><router-link :to="`/view_my_requests`">My Requests</router-link></h2><br>
        <h2 style="background-color: lightpink; padding: 10px;"><router-link :to="`/section_form`">Search Books by Section</router-link></h2><br>
    </div>
</template>

<script>
export default{
    mounted(){
        this.ready();
    },
    methods: {
        ready(){
            const token = localStorage.getItem("access_token");
            console.log(token);
            fetch("http://127.0.0.1:5000/user_dashboard",{
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
            .catch(error => {
                console.log(error);
            })
        }
    }
    
}
</script>