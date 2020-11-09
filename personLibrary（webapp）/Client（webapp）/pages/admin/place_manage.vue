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
				<text>读书广场</text>
			</view>
		</view>
		<view class="cu-bar bg-white solid-bottom" :class="isCard?'margin-top':''">
			<view class="action">
				<text class="cuIcon-titles text-orange "></text> 页面展开
			</view>
			<view class="action">
				<switch :class="isCard?'checked':''" :checked="isCard?true:false" @change="IsCard"></switch>
			</view>
		</view>
		<view class="cu-card dynamic" :class="isCard?'no-card':''">
			<view class="cu-item shadow">
				<view class="cu-item" style="height: 100upx;;">
					<view class="content flex-sub">
						<view class="flex justify-center align-center"><text style="font-size: 35upx;text-align: center;line-height: 100upx;"><strong>帖子管理</strong></text></view>
					</view>
				</view>

				<view v-for="(item,index) in invitation" :key="index" class="cu-list menu-avatar comment solids-top ">
					<view class="cu-item">
						<view class="cu-avatar round users_name">
							<image :src="item.wuserimage==null?'../../static/img/people_img.png':'item.wuserimage'"></image>
						</view>
						<view class="content">
							<view class="text-grey">{{item.wusername}}</view>
							<view class="text-gray text-content text-df">
								{{item.winvitate}}
							</view>
							<view class="bg-white padding-sm radius margin-top-sm  text-sm">
								<view class="flex book_content">
									<image :src="item.wbookimage"></image>
									<text style="text-align: center;">{{item.winvitatebookname}}</text>
								</view>
							</view>
							<view class="margin-top-sm flex justify-between">
								<view class="text-gray text-df">{{item.winvitatedate}}</view>
								<button @tap="godelete(item.wbookid,item.winvitatebookname)" style="margin-bottom: 5upx;" class="cu-btn bg-grey ">删除</button>
							</view>
						</view>
					</view>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	import helper from "../../common/until.js";
	export default {
		data() {
			return {
				isCard: false,
				invitation: []

			}
		},
		onLoad() {
			this.getinvitation();
		},
		methods: {
			godelete(bookid, name) {
				var bookname_1 = name;
				uni.showModal({
					title: '提示',
					content: '是否删除?',
					success: function(res) {
						if (res.confirm == true) {
							uni.showModal({
								title: "提示",
								content: '确认删除?',
								success: function(res) {
									if (res.confirm == true) {
										uni.request({
											url: helper.baseUrl+"/card/deletetalk",
											data: {
												bookname: bookname_1
											},
											method: "POST",
											success: (res) => {
												uni.showToast({
													icon: "success",
													title: res.data.desc
												})
											}
										})

									} else if (res.cancel == true) {

									}
								}
							})
						} else if (res.cancel == true) {

						}

					}
				})
			},
			getinvitation() {
				uni.request({
					url: helper.baseUrl+"/card/invitate",
					data: {

					},
					success: (res) => {
						this.invitation = res.data.invatate;
					}
				})
			},
			gomy(){
				var data=""
				try{
					const res=uni.getStorageSync("adminim");
					data =JSON.parse(res);
				} catch(e){
					
				}
				if(data==""){
					uni.showToast({
						icon:"none",
						title:"系统繁忙"
					})
					uni.reLaunch({
						url:"../login/admin-login"
					})
				}else{
					uni.reLaunch({
						url:"./admin"
					})
				}
				
			},
			IsCard(e) {
				this.isCard = e.detail.value
			},

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
	.users_name image {
		width: 60upx;
		height: 60upx;

	}

	.book_content {
		height: 100upx;
		line-height: 80upx;
		display: flex;
		background: #E5e5e5;
		border-radius: 7px;
		margin: 10upx 10upx;
		margin-bottom: 10upx;
		padding: 10upx 10upx;
		/* border: 1px solid #e4e4e4; */
	}

	.book_content image {
		width: 80upx;
		height: 80upx;
		/* background: #E5e5e5; */
		margin: 0 20upx;

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
