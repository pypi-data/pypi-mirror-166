class consolechars():
	russian_list = ['а','б','в','г','д','е','ё','ж','з','и','й','к','л','м','н','о','п','р','с','т','у','ф','х','ц','ч','ш','щ','ъ','ы','ь','э','ю','я']
	english_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

	russian = str(russian_list).replace(',', '').replace('\'', '').replace('[', '').replace(']', '').replace(' ', '')
	english = str(english_list).replace(',', '').replace('\'', '').replace('[', '').replace(']', '').replace(' ', '')
