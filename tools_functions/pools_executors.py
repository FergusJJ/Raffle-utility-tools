class Pool_Executor:

    def __init__(self):
        pass

    def process_pool(self):
        pass

    def thread_pool(self):
        pass
'''
   def get_links_from_email(self,amount_matching_criteria,login_session,substring_filter):
        sys.stdout.write(Style.MAGENTA)
        for message_num in self.amount_matching_criteria.split():
            counter += 1
            _, self.individual_response_data = self.login_session.fetch(message_num, '(RFC822)')
            self.raw = email.message_from_bytes(self.individual_response_data[0][1])
            raw = self.raw
            self.scraped_email_value = email.message_from_bytes(Mail.scrape_email(raw))
            self.scraped_email_value = str(self.scraped_email_value)
            self.returned_links = prog.findall(self.scraped_email_value)
                  
            for i in self.returned_links:
                if self.substring_filter in i:
                    Mail.link_set.add(i)
            self.timestamp = time.strftime('%H:%M:%S')
            print(f'[{self.timestamp}] Links scraped: [{counter}/{len(num_mails)}]')
            sys.stdout.write(Style.RESET)
            '''
'''
    def process_pool(self,amount_matching_criteria,login_session,substring_filter,function_name):
        
        futures = []
        
        with concurrent.futures.ProcessPoolExecutor() as E:
            for messages in self.amount_matching_criteria:
              
                task_params = self.amount_matching_criteria + self.login_session + self.substring_filter
            
                print(task_params)
                futures.append(
                    E.submit(
                        function_name, 
                        *task_params
                ))
                
            for future in concurrent.futures.as_completed(futures):
                print(future.result())


        if raw.is_multipart():
            
            return Mail.scrape_email(raw.get_payload(0))
        else:
            return raw.get_payload(None,True)
'''