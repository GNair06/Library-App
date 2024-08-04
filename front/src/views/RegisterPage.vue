<template>
    <div class="register container">
        <form @submit.prevent="register">
            <h1>Register</h1>
            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" v-model="email" required>
            </div>
            <div class="mb-3">
                <label for="name" class="form-label">name</label>
                <input type="text" class="form-control" id="name" v-model="name" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">password</label>
                <input type="password" class="form-control" id="password" v-model="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
        </form>
    </div>
</template>

<script>
export default{
    data(){
        return{
            email: '',
            name: '',
            password: '',
        }
    },
    methods:{
        async register(){
            try{
                const response = await fetch('http://localhost:5000/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        email: this.email,
                        name: this.name,
                        password: this.password,
                        role: this.role,
                    })
                });
                const data = await response.json();
                console.log(data);
                if (response.ok){
                    alert(data.message);
                    this.$router.push('/');
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