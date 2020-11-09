<template>
	<view>
		<!-- #ifdef APP-PLUS -->
		<view class="status_bar">
			<view class="top_view"></view>
		</view>
		<!-- #endif -->
		<view class="zhuce-top">
			<view @tap="gomy()" class="cuIcon-back cu-btn" style="padding-left: 10upx;background-color: #FFFFFF;">
				返回
			</view>
			<view class="book_place">
				<text>关于我们</text>
			</view>
		</view>
		<!-- <view class="cu-bar justify-center bg-white">
			<view class="action sub-title">
				<text class="text-xl text-bold text-blue">关于我们</text>
				<text class="text-ABC text-blue">about</text>
				<!-- last-child选择器-->
			<!-- </view>
		</view> --> 
		<view class="flex justify-center align-center" style="padding-top: 10upx;">
			<view class="bg-white" style="width: 700upx; border: 1px solid #e0e0e0;">
				<view class="cu-timeline">
					<view class="cu-item cur cuIcon-noticefill">
						<view class="content bg-green shadow-blur">
							<text>联系我们:</text> <br/>qq邮箱:1413502842@qq.com
						</view>
					</view>
					</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				
			}
		},
		methods: {
			gomy(){
				var data=""
				try{
					const res=uni.getStorageSync("userim");
					data =JSON.parse(res);
				} catch(e){
					
				}
				if(data==""){
					uni.showToast({
						icon:"none",
						title:"系统繁忙"
					})
					uni.removeStorage({
						key:"userim",
						success:function(res){
							
						},
						fail() {
							
						}
					})
					uni.reLaunch({
						url:"../login/login"
					})
				}else{
					uni.reLaunch({
						url:"./my"
					})
				}
				
			}
		}
	}
</script>

<style>
	.book_place {
		height: 70upx;
		text-align: center;
		line-height: 70upx;
		font-weight: bold;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
		margin-left: 200upx;
	}
	.zhuce-top {
		display: flex;
		height: 70upx;
		line-height: 70upx;
		border-bottom: 1px solid #e4e4e4;
		background-color: #FFFFFF;
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
