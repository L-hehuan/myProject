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
				<text>图书管理</text>
			</view>
		</view>
		<view class="cu-bar bg-white solid-bottom margin-top" style="margin-bottom: 10upx;">
			<view class="action">
				<text class="cuIcon-title text-orange "></text>书籍列表
			</view>
		</view>
		<view class="flex" style="">
			<scroll-view class="" scroll-y style="height: calc(100vh - 210upx);width: 200upx;">
				<view @tap="select(i)" :style="{fontSize:selected==i?'120%':'100%'}" :class="selected==i?'bg-white text-bold':''"
				 v-for="(p,i) in goods" :key="i" class="type-item">
					<view v-if="selected==i" class="shuxian"></view>{{p.wyname}}
				</view>
			</scroll-view>
			<scroll-view scroll-with-animation :scroll-into-view="'book-'+selected" class="bg-white" scroll-y style="height: calc(100vh - 210upx);width: 550upx;">
				<view :id="'book-'+i" v-for="(p,i) in goods" :key="i" class="" style="border-bottom: 0.5upx #e7e7e7 solid;padding-bottom: 40upx;">
					<view class="text-bold text-black g-title">
						{{p.wyname}}
					</view>
					<view class="flex flex-wrap ">
						<view v-for="(tp,ti) in p.data" :key="ti" class="flex justify-center align-center" style="width: 275upx;margin-top: 10upx;border: 1px #e0e0e0 solid;">
							<view class="">
								<image @tap="gotodetail(tp.wbookid)" style="width: 200upx;height: 300upx;" :src="tp.wbookimage"></image>
								<view class="flex justify-center align-center flex-direction">
									<view class="" style="text-align: center;width: 200upx;white-space: nowrap;overflow: hidden;text-overflow: ellipsis;">{{tp.wbookname}}</view>
									<view class="" style="text-align: center;width: 200upx;white-space: nowrap;overflow: hidden;text-overflow: ellipsis;">
										<button @tap="godelete(tp.wbookid,tp.wbookname)" style="margin-bottom: 5upx;" class="cu-btn bg-grey ">删除</button>
									</view>

								</view>

							</view>

						</view>
					</view>
				</view>
			</scroll-view>
		</view>
	</view>
</template>

<script>
	import helper from "../../common/until.js";
	export default {
		data() {
			return {
				booklists: "",
				goods: [],
				selected: 0,
				wusername: ""

			}
		},
		methods: {
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
			godelete(bookid,name) {
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
											url: helper.baseUrl+"/admin/book",
											data: {
												bookid: bookid
											},
											method:"POST",
											success: (res) => {
												uni.showToast({
													icon: "success",
													title: res.data.desc
												});
												try {
													const res = uni.getStorageSync('userim');
													data = JSON.parse(res);
													if(data.walimit==9){
														this.wusername = data.wadminname;
													} else if(data.walimit==999){
														this.wusername = data.wusername;
													}
												} catch (e) {
													//TODO handle the exception
												};
												uni.request({
													url: helper.baseUrl+"/mylike/delete",
													data: {
														bookname: bookname_1
													},
													method: "POST",
													success: (res) => {
														uni.showToast({
															icon: "success",
															title: res.data.desc
														})
													},
													fail: (res) => {
														uni.showToast({
															icon:"none",
															title:"网络连接失败"
														})
													}
												});
												uni.request({
													url: helper.baseUrl+"/card/deletetalk",
													data:{
														bookname:bookname_1
													},
													method:"POST",
													success: (res) => {
														uni.showToast({
															icon: "success",
															title: res.data.desc
														})
													},
													fail: (res) => {
														uni.showToast({
															icon:"none",
															title:"网络连接失败"
														})
													}
												})
											},
											fail: (res) => {
												uni.showToast({
													icon:"none",
													title:"网络连接失败"
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
			get_book() {
				var god=""
				var godim=[]
				var data=""
				uni.request({
					url: helper.baseUrl+"/user/types",
					data: {

					},
					success: (res) => {
						this.goods = res.data;
						god = JSON.stringify(res.data);
							uni.setStorage({
								key: "godim",
								data: god,
								success() {},
								fail() {}
							});
							try {
								const res = uni.getStorageSync('godim');
								data = JSON.parse(res);
								this.goods = data;
							} catch (e) {
								//TODO handle the exception
							};
						},
						fail: (res) => {
							try {
								const res = uni.getStorageSync('godim');
								data = JSON.parse(res);
								this.goods = data;
							} catch (e) {
								//TODO handle the exception
							};
						}
						
					
				})
			},
			gotodetail(id) {
				uni.navigateTo({
					url: `../bookdata/bookdata?id=${id}`
				})
			},
			select(i) {
				this.selected = i;
			}

		},
		onLoad() {
			this.get_book();
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
	.type-item {
		height: 100upx;
		text-align: center;
		line-height: 100upx;
		position: relative;
	}

	.shuxian {
		position: absolute;
		width: 12upx;
		height: 40upx;
		background-color: red;
		top: 30upx;
		left: 10upx;
	}
</style>
