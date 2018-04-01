using System.Collections;
using System.Collections.Specialized;
using System.Text;
using AutoMapper;
using Castle.Components.DictionaryAdapter;

namespace bevrand.testsuite.Helpers
{
    public static class CreateApiRequestString
    {
        public static string GetQueryStringFromModel<TInterface, TPoco>(TPoco request) where TPoco : TInterface
        {
            var requeststring = new StringBuilder();

            DictionaryAdapterFactory factory = new DictionaryAdapterFactory();
            IDictionary listDictionary = new ListDictionary();

            AutoMapper.Mapper.Initialize(c => c.CreateMap<TPoco, TInterface>());

            var adapter = factory.GetAdapter<TInterface>(listDictionary);
            AutoMapper.Mapper.Map(request, adapter);

            bool isFirst = true;

            foreach (DictionaryEntry dictionaryEntry in listDictionary)
            {
                if (dictionaryEntry.Value != null)
                {
                    string seperator = isFirst ? "?" : "&";
                    requeststring.Append($"{seperator}{dictionaryEntry.Key}={dictionaryEntry.Value}");

                    isFirst = false;
                }
            }

            Mapper.Reset();
            return requeststring.ToString();
        }
    }
}