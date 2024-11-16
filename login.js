class Auth {
    // 方法1：檢查用戶名密碼是否正確
    static async checkCredentials(email, password) {
        // 從測試用戶數據中找到對應email的用戶
        try{
            const response = await fetch('userData.json');
            const users = await response.json();
            const user = users[email];
            
            // 如果找到用戶且密碼正確
            if (user && user.password === password) {
                // 複製用戶數據（使用展開運算符...）
                const userData = {...user};
                console.log(`Log in: ${userData.name}`)
                // 刪除密碼（不存儲敏感信息）
                delete userData.password;
                // 返回用戶數據
                return userData;
            }
        } catch (error) {
            console.error('Error checking credentials:', error);
            return null;
        }
        // 如果驗證失敗，返回null
        return null;
    }

    // 方法2：檢查是否已登入
    static isLoggedIn() {
        // 從localStorage檢查登入狀態
        return localStorage.getItem('isLoggedIn') === 'true';
    }

    // 方法3：執行登入操作
    static login(userData) {
        // 在localStorage設置登入狀態為true
        localStorage.setItem('isLoggedIn', 'true');
        // 存儲用戶數據
        localStorage.setItem('userData', JSON.stringify(userData));
    }

    // 方法4：執行登出操作
    static logout() {
        // 清除登入狀態
        localStorage.removeItem('isLoggedIn');
        // 清除用戶數據
        localStorage.removeItem('userData');
    }

    // 方法5：獲取當前登入用戶的數據
    static getUserData() {
        // 從localStorage獲取並解析用戶數據
        return JSON.parse(localStorage.getItem('userData'));
    }

    static isQualified() {
        // check if the user is qualified for medical need waiver
        if (!this.isLoggedIn()) {
            return false;
        }
        const userData = this.getUserData();
        return userData.qualification;
    }
}