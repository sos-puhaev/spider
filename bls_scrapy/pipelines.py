# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from pymongo import MongoClient

class BlsScrapyPipeline:

    def process_item(self, item, spider):

        # check entries via magnet link, it is unique
        magnet = item['torrents'][0]['magnet']

        # Connect in MongoDB
        client = MongoClient("mongo")
        db = client['mongo_db']
        collection = db['bls_scrapy']
        adult = False

        # Check for adult content
        if item['category'] == 'Porn':
            adult = True
        else:
            adult = False

        
        ex_record = collection.find_one({'magnet' : magnet})
        if ex_record:
            collection.update_one({'magnet': magnet}, {
                '$set':{
                    'title':item['torrents'][0]['title'],
                    'size': item['torrents'][0]['size'],
                    'category': item['category'],
                    'sub_category': item['torrents'][0]['sub_category'],
                    'url': item['torrents'][0]['url'],
                    'peers':item['torrents'][0]['peers'],
                    'seeds':item['torrents'][0]['seeds'],
                    'is_verified': item['torrents'][0]['verified'],
                    'date': item['torrents'][0]['released'],
                    'adult': adult,
                    'source': 'thepirate_bay',
                    'magnet': item['torrents'][0]['magnet'],
                    }
                })
        else:
            collection.insert_one({
                'title':item['torrents'][0]['title'],
                'size': item['torrents'][0]['size'],
                'category': item['category'],
                'sub_category': item['torrents'][0]['sub_category'],
                'url': item['torrents'][0]['url'],
                'peers':item['torrents'][0]['peers'],
                'seeds':item['torrents'][0]['seeds'],
                'is_verified': item['torrents'][0]['verified'],
                'date': item['torrents'][0]['released'],
                'adult': adult,
                'source': 'thepirate_bay',
                'magnet': item['torrents'][0]['magnet'],
            })

            
        # View entries from mongo

        # all_documents = collection.find()
        # print("------------------------------")
        # for document in all_documents:
        #     print(document)
        # print("------------------------------")
        client.close()

        return item
