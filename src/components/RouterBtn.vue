<template>
	<router-link :to="path" class="button">
		{{ buttonText }}
	</router-link>
</template>


<script setup>

const props = defineProps({
	path: {
		type: String,
		required: true
	},
	buttonText: {
		type: String,
		required: true
	}
});

</script>


<style scoped>

.button {
	display: inline-block;
	padding: 10px 20px;
	color: white;
	background-color: #007bff;
	border: none;
	border-radius: 4px;
	text-align: center;
	text-decoration: none;
	font-size: 16px;
}

.button:hover {
	background-color: #0056b3;
}

</style>