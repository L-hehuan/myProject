<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">  
		    <view class="top_view"></view>  
		</view>  
		<!-- #endif -->
		<view class="userim-top">
			<view @tap="gocard()" class="cuIcon-back cu-btn" style="padding-left: 10upx;background-color: #FFFFFF;">
				读书广场
			</view>
			<view class="book_place" style="padding-left: 10upx;">
				<text >评论页</text>
			</view>
			
		</view>
		<form>
			<view class="cu-form-group margin-top">
				<view class="title">书籍名</view>
				<input placeholder="请输入书籍名/注意:不能输错!!!" name="input" v-model="form.bookname"></input>
			</view>
			<view class="cu-form-group margin-top">
				<view class="title">对该书的评分</view>
				<input placeholder="请输入0-5分" name="input" v-model="form.star"></input>
			</view>
			<view class="cu-form-group align-start">
				<view class="title">评论栏</view>
				<textarea v-model="form.content" maxlength="-1" :disabled="modalName!=null" input="" placeholder="请输入你的留言信息"></textarea>
			</view>
			<view class="flex justify-center" style="margin-top: 40upx;">
				<button @tap="tijiao()" class="bg-gradual-red round" style="width: 650upx;">
					发表意见
				</button>
			</view>
		
		</form>
	</view>
</template>

<script>
	import helper from "../../common/until.js";
	export default {
		data() {
			return {
				text: 'uni-app',
				index: -1,
				modalName: null,
				wusername:"",
				form:{
					bookname:"",
					content:"",
					username:"",
					star:"",
					
				},
				mylists:{name:"my",
				         url:"../my/my",
				}
				
			}
		},
		onLoad() {
			setTimeout(function() {
			}, 1000);
			//uni.startPullDownRefresh();
			uni.startPullDownRefresh({
				success: function(res) { //success 返回参数说明
				}
			}); //这里表示当进入页面的时候就开始执行下拉刷新动画
		},
		onPullDownRefresh() {
			//监听下拉刷新动作的执行方法，每次手动下拉刷新都会执行一次
			setTimeout(function() {
				uni.stopPullDownRefresh(); //停止下拉刷新动画
			}, 1000);
			this.godeltalk();
		},
		
		methods: {
			godeltalk(){
				this.form.bookname="";
				this.form.content="";
				this.form.star="";
			},
			tijiao(){
				var data="";
				var fu_name="";
				var numlist=[0,1,2,3,4,5];
				if(this.form.bookname=="" || this.form.star==0 || this.form.content==""){
						uni.showToast({
							icon:"none",
							title:"请检查你的输入是否有空项"
						})
				}else{
					if(this.form.star in numlist){
					try {
						const res = uni.getStorageSync('userim');
						data = JSON.parse(res);
						this.form.username = data.wusername;
						
					} catch (e) {
						//TODO handle the exception
					};
					uni.request({
						url: helper.baseUrl+"/card/talk",
						data:{
							bookname:this.form.bookname,
							name:this.form.username,
							star:this.form.star,
							content:this.form.content
						},
						method:"POST",
						success: (res) => {
							if(res.data.status==0){
								uni.showToast({
								icon:"none",
								title:res.data.desc
							});
							this.form.bookname="";
							this.form.content="";
							this.form.star="";
							uni.reLaunch({
								url:"./card"
							})}else{
								uni.showToast({
									icon:"none",
									title:res.data.desc
								});
							}
							
						},
						fail: (res) => {
							uni.showToast({
								icon:"none",
								title:"网络连接出错"
							})
						}
					})
					}else{
						uni.showToast({
							icon:"none",
							title:"请检查你的输入是否有误"
						})
					}
					
				}
				
			},
			gocard() {
				var url = "../card/card";
				if (url != null && url != undefined) {
					uni.reLaunch({
						url: url
					});
				}
			
			},
		}
	}
</script>

<style>
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
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
		margin-left: 120upx;
	}
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

</style>
