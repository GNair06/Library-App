<template>
<div>
    <NavComp/>
    <div class="login container">
        <form @submit.prevent="login">
            <h1>Login</h1>
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" v-model="email" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">password</label>
                <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</div>
</template>

<script>
import NavComp from '@/components/NavComp.vue'
export default{

    data(){
        return{
            email: '',
            password: '',
        }
    },
    components: {
        NavComp
    },
    methods:{
        async login(){
            try{
                const response = await fetch('http://localhost:5000/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        password: this.password,
                    })
                });
                const data = await response.json();
                console.log(data);
                if (response.ok){
                    alert(data.message);
                    // 2 types of storage - local and session
                    // store access token in local storage
                    localStorage.setItem("access_token", data.access_token); 
                    //redirect to home page
                    this.$router.push('/dashboard');
                }
                else{
                    alert(data.error);
                }
            } catch (error){
                console.log(error);
                alert('some error occurred')
            }

        }
    }
};
</script>