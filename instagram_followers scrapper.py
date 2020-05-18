from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd

user_n = input("TYPE THE USER NAME OF THE ACCOUNT (it should be accurate)--> ")
passwd = input("TYPE PASSWORD OF THE ACCOUNT --> ")
acc_to_scrape = input("TYPE THE ACCOUNT TO SCRAPE --> ")
ask_file = input("DO YOU WANT TO STORE DATA IN CSV FILE? [y/n] -->")
file_n = ''
if ask_file.lower() == 'y':
    file_n = input('ENTER THE FILE NAME (ex: My File)---> ')


def instagram_followers_scraper(username, password, account_to_scrape, file, file_name):
    driver = webdriver.Chrome()
    a, b = True, True
    print('----STARTED------')
    print('NOTE: IF THERE ARE TOO MANY FOLLOWERS THIS COULD TAKE SOME TIME SO BE PATIENT')

    driver.get("https://www.instagram.com/")

    u_id = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".FBi-h+ .-MzZI .zyHYP"))
    )

    u_id.clear()
    u_id.send_keys(username)  # username

    pwd = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".-MzZI+ .-MzZI .zyHYP"))
    )
    pwd.clear()
    pwd.send_keys(password)  # password

    login_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".-MzZI+ .DhRcB"))
    )
    login_button.click()
    try:
        not_now = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div/div/div[3]/button[2]"))
        )
        not_now.click()
    except TimeoutException:
        a = False
        return "----------U DIDN'T ENTERED CORRECT USER_ID OR PASSWORD-------------"

    if a:
        try:
            driver.get('https://www.instagram.com/{0}/'.format(account_to_scrape))
        except TimeoutException:
            b = False
            return "--------THE ACCOUNT YOU ENTERED TO SCRAPE IS INCORRECT---------"

        if b:
            followers = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".Y8-fY:nth-child(2) .-nal3"))
            )

            followers.click()

            nu_of_followers = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a/span')))
            n_o_f = int(nu_of_followers.text)
            print('Number of Followers are : ', n_o_f)
            fBody = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='isgrP']"))
            )
            scroll = 0
            while scroll < n_o_f // 5:
                driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
                time.sleep(1)
                scroll += 1

            fList = driver.find_elements_by_xpath("//div[@class='isgrP']//li")
            print(fList)
            print("fList len is {}".format(len(fList)))
            user_name = []
            name = []

            for f in fList:
                s = f.text
                l = s.split('\n')
                user_name.append(l[0])
                name.append(l[1])

            # print(user_name, '\n', name)
            followers_data = pd.DataFrame({
                'USER_NAMES': user_name,
                'NAME': name
            })
            driver.close()
            if file == 'y':
                followers_data.to_csv(file_name + ".csv")
                return '------ENDED------'
            else:
                pass
                return '------ENDED------'


print(instagram_followers_scraper(user_n, passwd, acc_to_scrape, ask_file.lower(), file_n))

# username = "jennifergoenka"
# password = '111213'
