<template>
	<view>
		<!-- #ifdef APP-PLUS -->  
		<view class="status_bar">  
		    <view class="top_view"></view> 
		</view>  
		<!-- #endif -->
		<view class="xiding" :style="{'margin-top':barHeight+'px'}">
			<view class="cu-bar" style="position: fixed;top:12upx;width: 750upx;z-index: 9999;">
				<view @tap="goindex()" class="action anniu">
					<view class="action cuIcon-back text-white" style="font-size: 160%;color: white;">
					</view>

				</view>

			</view>
		</view>
		<view style="padding: 10upx 10upx;border: 2upx solid #e0e0e0;">
			<image mode="widthFix" class="banerimg" :src="detail.wbookimage"></image>
		</view>
		<view style="padding: 10upx 10upx;border: 2upx solid #e0e0e0;" class="bg-white flex justify-between">
			<view class="text-red">
				<text style="font-weight: 900;">书名:</text>
				<text class="text-black">{{detail.wbookname}}</text>
			</view>
		</view>
		<view style="padding: 10upx 10upx;border: 2upx solid #e0e0e0;" class="bg-white flex justify-between">
			<view class="flex">
				<view class="text-red">
					<text style="font-weight: 900;">分类:</text>
				</view>

				<text class="text-black">{{rcategory.wyname}}</text>
			</view>
		</view>
		<view style="padding: 10upx 10upx;border: 2upx solid #e0e0e0;" class="bg-white flex justify-between">
			<view class="text-red">
				<text style="font-weight: 900;">作者:</text>
				<text class="text-black">{{detail.wbookauthor}}</text>
			</view>
		</view>
		<view style="padding: 10upx 10upx;border: 2upx solid #e0e0e0;" class="bg-white flex justify-between">
			<view class="text-red ">
				<view class="" style="border-bottom: 2upx solid #e0e0e0;">
					<text style="font-weight: 1000;">简介</text>
				</view>
				<text class="text-black">{{detail.wbookpdesc}}</text>
			</view>
		</view>
		<view class="xidengbuttom">

		</view>
		<view class="barfixed cu-bar bg-white tabbar border shop">
			<view @tap="addmyfavious()" class="bg-orange submit">加入我的收藏</view>
			<view @tap="readbook(detail.wbookid)" class="bg-red submit">阅读此书</view>
			<view @tap="gocards()" class="bg-yellow submit" style="color: white;">去读书广场</view>
		</view>
	</view>
</template>

<script>
	import helper from "../../common/until.js"
	export default {
		data() {
			return {
				text: 'uni-app',
				wbookid: "",
				detail: {

				},
				barHeight:25,
				wusername: "",
				bookname: "",
				rcategory: {

				}
			}
		},
		methods: {
			getdata() {
				uni.request({
					url: helper.baseUrl + "/book/detail",
					data: {
						id: this.wbookid
					},
					method: "GET",
					success: (res) => {
						// console.log(res.data.detail);
						// console.log(res.data.rcategory);
						this.detail = res.data.detail;
						this.rcategory = res.data.rcategory;
						this.bookname = res.data.detail.wbookname;
					},
					fail: (res) => {
						uni.showToast({
							icon:"none",
							title:"网络连接出错"
						})
					}
				})
			},
			goindex() {
				uni.reLaunch({
					url: "../card/card",
					animationType: 'pop-in',
					animationDuration: 200
				})
			},
			readbook(bookid) {
				var data = "";
				var book_content = "";
				uni.showModal({
					title: '提示',
					content: '前往阅读?',
					success: function(res) {
						if (res.confirm == true) {
							try {
								const res = uni.getStorageSync('userim');
								data = JSON.parse(res);
							} catch (e) {
								//TODO handle the exception
							};
							if (data != "") {
								uni.request({
									url: helper.baseUrl + "/book/read",
									data: {
										bookid: bookid
									},
									method: "POST",
									success: (res) => {
										if (res.data.status == 0) {
											book_content = JSON.stringify(res.data);
											uni.setStorage({
												key: "bookim",
												data: book_content,
												success() {
													// console.log("成功了");
													uni.navigateTo({
														url: "./bookread",
														animationType:"slide-in-bottom",
														animationDuration:500
													})
												},
												fail() {
													// console.log('失败了')
												}
											});
										} else {

										}

									},
									fail: (res) => {
										uni.showToast({
											icon:"none",
											title:"网络连接出错"
										})
									}
								})

							} else {
								uni.showModal({
									title: '提示',
									content: '未登录,是否进行登录',
									success: function(res) {
										if (res.confirm == true) {
											uni.navigateTo({
												url: "../login/login",
												animationType:"zoom-out",
												animationDuration:500
											})
										} else if (res.cancel == true) {
											uni.showToast({
												icon: "none",
												title: "取消登录"
											})
										}
									}
								});
							}
						} else if (res.cancel == true) {}
					}
				});
			},
			gocards() {
				uni.showModal({
					title: '提示',
					content: '前往读书广场?',
					success: function(res) {
						if (res.confirm == true) {
							uni.reLaunch({
								url: "../card/card"
							})
						} else if (res.cancel == true) {}
					}
				});

			},
			addmyfavious() {
				var data = "";
				var bookname_1 = this.bookname;
				uni.showModal({
					title: '提示',
					content: '确定添加到收藏夹?',
					success: function(res) {
						if (res.confirm == true) {
							try {
								const res = uni.getStorageSync('userim');
								data = JSON.parse(res);
								if (data.walimit == 9) {
									this.wusername = data.wusername;
								} else if (data.walimit == 99) {
									this.wusername = data.wusername;
								} else if(data.walimit == 999){
									this.wusername = data.wadminname;
								}
							} catch (e) {
								//TODO handle the exception
							};
							if (data != "") {
								uni.request({
									url: helper.baseUrl + "/goods/chaxun",
									data: {
										username: this.wusername,
										bookname: bookname_1,

									},
									method: "POST",
									success: (res) => {
										if (res.data.status == 1) {
											uni.showToast({
												icon: "none",
												title: res.data.desc
											})
										} else if (res.data.status == 0) {
											uni.request({
												url: helper.baseUrl + "/my/like",
												data: {
													username: this.wusername,
													bookname: bookname_1,
												},
												method: "POST",
												success: (res) => {
													if (res.data.status == 0) {
														uni.showToast({
															icon: "success",
															title: res.data.desc
														})
													} else {
														uni.showToast({
															icon: "none",
															title: res.data.desc
														})
													}

												}
											})

										}
									},
									fail: (res) => {
										uni.showToast({
											icon:"none",
											title:"网络连接出错"
										})
									}
								})

							} else {
								uni.showModal({
									title: '提示',
									content: '未登录,是否进行登录',
									success: function(res) {
										if (res.confirm == true) {
											uni.navigateTo({
												url: "../login/login",
												animationType:"zoom-out",
												animationDuration:500
											})
										} else if (res.cancel == true) {
											uni.showToast({
												icon: "none",
												title: "取消登录"
											})
										}
									}
								});
							}
						} else if (res.cancel == true) {}
					}
				});

			},
		},
		onLoad(options) {
			this.wbookid = options.id;
			this.getdata();
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
			this.getdata();
		},
		
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
	.barfixed {
		position: fixed;
		bottom: 0upx;
		width: 750upx;
	}

	.xiding {
		width: 100%;
		height: var(--status-bar-height);
	}

	.xidengbuttom {
		height: calc(100upx + env(safe-area-inset-bottom) / 2);
		width: 100%;
		min-height: 100upx;
	}

	.banerimg {
		width: 750upx;
	}

	.anniu {
		width: 80upx;
		height: 80upx;
		padding: 8upx 8upx;
		border-radius: 80upx;
		display: flex;
		justify-content: center;
		align-items: center;
		background-color: rgba(41, 36, 33, 0.2);
	}
</style>
