import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class BossSpider(scrapy.Spider):
    name = "bossSpider"
    # 设置输出文件
    custom_settings = {
        'FEED_URI': 'BossData.csv',
    }
    # 创建WebDriver实例，不能开启无头模式，否则无法获取到数据
    driver = webdriver.Edge()
    query = input("输入要搜索的职位、公司：")
    page = 1

    def start_requests(self):
        url = f"https://www.zhipin.com/web/geek/job?query={self.query}&city=100010000"
        self.driver.get(url)
        yield scrapy.Request(url, callback=self.parse, meta={'driver': self.driver})

    def parse(self, response, **kwargs):
        driver = response.meta['driver']
        try:
            # 等待元素加载成功
            WebDriverWait(driver, 60).until(
                ec.presence_of_element_located(
                    (By.XPATH, '//div[@class="search-job-result"]//li[@class="job-card-wrapper"]'))
            )
            job_elements = driver.find_elements(By.XPATH,
                                                '//div[@class="search-job-result"]//li[@class="job-card-wrapper"]')
            for element in job_elements:
                data_store = DataStore()
                # 职位名称
                data_store['name'] = element.find_element(By.XPATH, './/span[@class="job-name"]').text
                # 工作地点
                data_store['area'] = element.find_element(By.XPATH, './/span[@class="job-area"]').text
                # 薪水
                data_store['salary'] = element.find_element(By.XPATH, './/span[@class="salary"]').text
                # 标签(经验、学历)
                tag = element.find_element(By.XPATH, './/ul[@class="tag-list"]')
                tag_list = tag.find_elements(By.TAG_NAME, 'li')
                data_store['experience'] = tag_list[0].text
                data_store['education'] = tag_list[1].text
                # 联系人
                data_store['contact_person'] = element.find_element(By.XPATH, './/div[@class="info-public"]').text
                # 公司logo
                company_logo = element.find_element(By.XPATH, './/div[@class="company-logo"]')
                logo_img = company_logo.find_element(By.TAG_NAME, 'a').get_attribute('href')
                data_store['company_logo'] = logo_img
                # 公司名称
                data_store['company_name'] = element.find_element(By.XPATH, './/h3[@class="company-name"]').text
                # 公司标签
                company_tag_list = element.find_element(By.XPATH, './/ul[@class="company-tag-list"]')
                tag_list = company_tag_list.find_elements(By.TAG_NAME, 'li')
                data_store['company_tag'] = ','.join([tag.text for tag in tag_list if tag.text])
                # 职位描述
                footer = element.find_element(By.XPATH, './/div[@class="job-card-footer clearfix"]')
                tag_list = footer.find_elements(By.TAG_NAME, 'li')
                data_store['tag_list'] = ','.join([tag.text for tag in tag_list if tag.text])
                # 公司福利
                data_store['info_desc'] = footer.find_element(By.XPATH, './/div[@class="info-desc"]').text

                yield data_store.data

            self.page += 1
            if self.page <= 3:
                next_page_url = f"https://www.zhipin.com/web/geek/job?query={self.query}&city=100010000&page={self.page}"
                self.driver.get(next_page_url)
                yield scrapy.Request(next_page_url, callback=self.parse, meta={'driver': self.driver})

        except Exception as e:
            # 处理超时异常或其他异常
            print(f"Error: {e}")
            yield None


# 存储抓到的数据
class DataStore:
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, item):
        return self.data[item]
