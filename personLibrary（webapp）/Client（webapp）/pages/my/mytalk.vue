<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="userim-top">
			<view @tap="gomy()" class="cuIcon-back cu-btn" style="padding-left: 10upx;background-color: #FFFFFF;">
				我的主页
			</view>
			<view class="book_place" style="padding-left: 10upx;">
				<text >留言反馈</text>
			</view>
			
		</view>
		<view class="cu-form-group margin-top">
			<view class="title">反馈标题</view>
			<input type="text" placeholder="不超过八个字" value="" v-model="form.title"/>
		</view>
		<view class="cu-form-group align-start">
			<view class="title">反馈栏</view>
			<textarea v-model="form.content" maxlength="-1" :disabled="modalName!=null" input="" placeholder="请输入你的留言信息"></textarea>
		</view>
		<view class="flex justify-center" style="margin-top: 40upx;">
			<button @tap="tijiao()" class="bg-gradual-red round" style="width: 650upx;">
				提交反馈
			</button>
		</view>
	</view>
</template>

<script>
	import helper from "../../common/until.js"
	export default {
		data() {
			return {
				index: -1,
				modalName: null,
				form:{
					title:"",
					content:"",
					title_id:""
				},
				mylists:{name:"my",
				         url:"../my/my",
				}
			}
		},
		methods: {
			tijiao(){
				var data="";
				try {
					const res = uni.getStorageSync('userim');
					data = JSON.parse(res);
					this.form.title_id=data.wuserid;
				} catch (e) {
					//TODO handle the exception
				};
				if(data!=""){
					if(this.form.title.length>8 || this.form.content=="" || this.form.title==""){
						uni.showToast({
							icon:"none",
							title:"格式有误"
						})
					}else{
						uni.request({
							url:helper.baseUrl+"/my/message",
							data:{
								message_title:this.form.title,
								message_content:this.form.content,
								message_id:this.form.title_id
								},
							method:"POST",
							success: (res) => {
								uni.showToast({
									icon:"success",
									title: res.data.desc
								});
								uni.reLaunch({
									url:"../my/my"
								})
							},
							fail() {
								uni.showToast({
									icon:"none",
									title:"网络连接失败"
								})
							}
						})
					}
				}else{
					uni.showToast({
						icon:"none",
						title:"登录失效"
					})
					uni.removeStorage({
						key:"userim",
						success: () => {
							
						},
						fail: () => {
							
						}
					})
					uni.reLaunch({
						url:"../login/login"
					})
				}
				
				
				
			},
			gomy(){
				var url=this.mylists.url;
				if(url!=null&&url!=undefined){
					uni.reLaunch({
						url:url
					});
				}
				
			},
		}
	}
</script>

<style>
	.status_bar {
	    height: var(--status-bar-height);  
	    width: 100%;  
	    background-color: #F8F8F8;  
	}  
	.top_view {  
	    height: var(--status-bar-height);  
	    width: 100%;  
	    position: fixed;  
	    background-color: #F8F8F8;  
	    top: 0;  
	    z-index: 999;  
	}
	.userim-top{
		display: flex;
		height: 70upx;
		line-height: 70upx;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
	}
	.book_place {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		font-weight: bold;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
		margin-left: 120upx;
	}

</style>
